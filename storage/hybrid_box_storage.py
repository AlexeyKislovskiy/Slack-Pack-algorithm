import math
from functools import cmp_to_key
from sortedcontainers import SortedSet
from sqlalchemy import Column, Integer, Float, String, create_engine, MetaData, Table, Index, insert, Row
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from detail.detail import Detail
from storage.abstract_box_storage import BoxStorage


class HybridBoxStorage(BoxStorage):
    """
    A class representing a hybrid storage combining in-memory and database storage for boxes.

    This hybrid storage uses three caches:
    - `to_add_cache`: A cache for storing boxes to be added to the database.
    - `to_delete_cache`: A cache for storing boxes to be deleted from the database.
    - `max_cache`: A cache for storing the largest boxes retrieved from the database.

    Attributes:
        engine (Engine): The SQLAlchemy engine for connecting to the database.
        session (Session): The SQLAlchemy session for interacting with the database.
        boxes_table (Table): The SQLAlchemy Table object representing the boxes table.
        cache_size (int): The maximum size of the in-memory cache.
        to_add_cache (SortedSet[Detail]): A sorted set of boxes to be added to the database.
        max_cache (SortedSet[Detail]): A sorted set of the largest boxes retrieved from the database.
        to_delete_cache (list[Detail]): A list of boxes to be deleted from the database.
    """

    def __init__(self, db_url: str, table_name: str = 'boxes', cache_size: int = 1000000):
        """
        Initializes the HybridBoxStorage with the given database URL, table name, and cache size.

        :param db_url: The URL of the database to connect to.
        :param table_name: The name of the table to store boxes (default is 'boxes').
        :param cache_size: The maximum size of the in-memory cache.
        """
        self.engine = create_engine(db_url)
        metadata = MetaData()
        self.boxes_table = Table(table_name, metadata,
                                 Column('id', Integer, primary_key=True, autoincrement=True),
                                 Column('bottom_left_x', Float),
                                 Column('bottom_left_y', Float),
                                 Column('top_right_x', Float),
                                 Column('top_right_y', Float),
                                 Column('min_size', Float),
                                 Column('name', String),
                                 Column('detail_type', String),
                                 Index('idx_min_size', 'min_size'))
        self._drop_existing_table()
        metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        self.cache_size = cache_size
        self.to_add_cache = SortedSet(key=cmp_to_key(self._detail_comparator))
        self.max_cache = SortedSet(key=cmp_to_key(self._detail_comparator))
        self.to_delete_cache = []

    def _drop_existing_table(self) -> None:
        """
        Drop the existing table with the specified table name if it exists.
        """
        try:
            self.boxes_table.drop(self.engine)
        except ProgrammingError:
            pass

    def add_box(self, detail: Detail) -> None:
        """
        Add a box to the hybrid storage.

        :param detail: A Detail object representing the box to be added to the storage.
        """
        self.to_add_cache.add(detail)
        if len(self.to_add_cache) > self.cache_size:
            self._update_caches()

    def get_max_box(self) -> Detail:
        """
        Retrieve the largest box from the hybrid storage without removing it.

        :return: The largest box.
        """
        max_from_to_add_cache = self.to_add_cache[0] if len(self.to_add_cache) > 0 else None
        max_from_max_cache = self.max_cache[0] if len(self.max_cache) > 0 else None
        return max_from_max_cache \
            if self._detail_comparator(max_from_to_add_cache, max_from_max_cache) >= 0 \
            else max_from_to_add_cache

    def pop_max_box(self) -> Detail:
        """
        Retrieve and remove the largest box from the hybrid storage.

        :return: The largest box.
        """
        max_from_to_add_cache = self.to_add_cache[0] if len(self.to_add_cache) > 0 else None
        max_from_max_cache = self.max_cache[0] if len(self.max_cache) > 0 else None
        if self._detail_comparator(max_from_to_add_cache, max_from_max_cache) >= 0:
            self.to_delete_cache.append(self.max_cache.pop(0))
            if len(self.max_cache) == 0:
                self._update_caches()
            return max_from_max_cache
        else:
            self.to_add_cache.pop(0)
            return max_from_to_add_cache

    def _update_caches(self) -> None:
        """
        Update all caches by syncing the in-memory caches with the database.

        This method is triggered under two conditions:
        1. When `to_add_cache` exceeds its defined `cache_size`.
        2. When `max_cache` becomes empty.
        """
        self._update_to_add_cache()
        self._update_to_delete_cache()
        self._update_max_cache()

    def _update_to_add_cache(self) -> None:
        """
        Update the `to_add_cache` by inserting its contents into the database.
        """
        BATCH_SIZE = 1000000
        values = [
            {
                'bottom_left_x': detail.bottom_left[0],
                'bottom_left_y': detail.bottom_left[1],
                'top_right_x': detail.top_right[0],
                'top_right_y': detail.top_right[1],
                'min_size': min(detail.width, detail.height),
                'name': detail.name,
                'detail_type': detail.detail_type
            }
            for detail in self.to_add_cache
        ]
        for i in range(0, len(values), BATCH_SIZE):
            batch = values[i:i + BATCH_SIZE]
            self.session.execute(insert(self.boxes_table), batch)
            self.session.commit()
        self.to_add_cache = SortedSet(key=cmp_to_key(self._detail_comparator))

    def _update_to_delete_cache(self) -> None:
        """
        Update the `to_delete_cache` by deleting its contents from the database.
        """
        detail_names = [detail.name for detail in self.to_delete_cache]
        self.session.query(self.boxes_table).filter(self.boxes_table.c.name.in_(detail_names)).delete(
            synchronize_session=False)
        self.session.commit()
        self.to_delete_cache = []

    def _update_max_cache(self) -> None:
        """
        Update the `max_cache` by retrieving the largest boxes from the database.
        """
        self.max_cache = SortedSet(key=cmp_to_key(self._detail_comparator))
        rows = self.session.query(self.boxes_table).order_by(self.boxes_table.c.min_size.desc()) \
            .limit(self.cache_size).all()
        for row in rows:
            self.max_cache.add(self._row_to_detail(row))

    @staticmethod
    def _detail_comparator(detail1: Detail, detail2: Detail) -> float:
        """
        Compares two details based on their minimum side length.

        :param detail1: The first detail for comparison.
        :param detail2: The second detail for comparison.
        :return: Positive if detail1 is larger, negative if detail2 is larger, 0 if equal.
        """
        if detail1 is None and detail2 is None:
            return 0
        if detail1 is None:
            return math.inf
        if detail2 is None:
            return -math.inf
        return min(detail2.width, detail2.height) - min(detail1.width, detail1.height)

    @staticmethod
    def _row_to_detail(row: Row) -> Detail:
        """
        Convert a row from the boxes table to a Detail object.

        :param row: The row representing a box in the database.
        :return: A Detail object representing the box.
        """
        return Detail(
            (row.bottom_left_x, row.bottom_left_y),
            (row.top_right_x, row.top_right_y),
            row.name,
            row.detail_type
        )
