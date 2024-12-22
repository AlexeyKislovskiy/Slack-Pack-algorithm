from sqlalchemy import Column, Integer, Float, String, create_engine, MetaData, Table, Index, Row
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from detail.detail import Detail
from storage.abstract_box_storage import BoxStorage


class DatabaseBoxStorage(BoxStorage):
    """
    A class representing a database storage for storing boxes during the detail placement process.

    Attributes:
        engine (Engine): The SQLAlchemy engine for connecting to the database.
        session (Session): The SQLAlchemy session for interacting with the database.
        boxes_table (Table): The SQLAlchemy Table object representing the boxes table.
    """

    def __init__(self, db_url, table_name='boxes'):
        """
        Initializes the DatabaseBoxStorage with the given database URL and table name.

        :param db_url: The URL of the database to connect to.
        :param table_name: The name of the table to store boxes (default is 'boxes').
        """
        self.engine = create_engine(db_url)
        metadata = MetaData()
        self.boxes_table = Table(table_name, metadata,
                                 Column('id', Integer, primary_key=True),
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
        Add a box to the database storage.

        :param detail: A Detail object representing the box to be added to the storage.
        """
        self.session.execute(self.boxes_table.insert().values(
            bottom_left_x=detail.bottom_left[0],
            bottom_left_y=detail.bottom_left[1],
            top_right_x=detail.top_right[0],
            top_right_y=detail.top_right[1],
            min_size=min(detail.width, detail.height),
            name=detail.name,
            detail_type=detail.detail_type
        ))
        self.session.commit()

    def get_max_box(self) -> Detail:
        """
        Retrieve the largest box from the database storage without removing it.

        :return: The largest box.
        """
        max_box = self.session.query(self.boxes_table).order_by(self.boxes_table.c.min_size.desc()).first()
        return self._row_to_detail(max_box) if max_box else None

    def pop_max_box(self) -> Detail:
        """
        Retrieve and remove the largest box from the database storage.

        :return: The largest box.
        """
        max_box = self.session.query(self.boxes_table).order_by(self.boxes_table.c.min_size.desc()).first()
        if max_box:
            self.session.query(self.boxes_table).filter_by(id=max_box.id).delete()
            self.session.commit()
            return self._row_to_detail(max_box)
        return None

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
