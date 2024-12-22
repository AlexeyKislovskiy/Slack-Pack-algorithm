from detail.detail import Detail
import json


def find_all_neighbours(details: list[Detail], target_detail: Detail) -> list[Detail]:
    """
    Find all neighboring detail of a target detail, including the target detail itself.
    Neighboring detail are those that share common points with the target detail.

    :param details: A list of Detail objects representing the detail to search within.
    :param target_detail: The target detail for which neighboring detail are to be found.
    :return: A list containing all neighboring detail of the target detail, including the target detail itself.
    """
    target_bottom_left_x, target_bottom_left_y = target_detail.bottom_left
    target_top_right_x, target_top_right_y = target_detail.top_right
    return [detail for detail in details
            if (target_bottom_left_x <= detail.top_right[0] and target_top_right_x >=
                detail.bottom_left[0])
            and (target_bottom_left_y <= detail.top_right[1] and target_top_right_y >=
                 detail.bottom_left[1])]


def find_neighbours_of_depth(details: list[Detail], target_detail: Detail, depth: int) -> list[Detail]:
    """
    Find neighboring detail of a target detail up to a specified depth.
    If the depth is 0, only the target detail itself is returned. If the depth is 1, the target detail and
    its immediate neighbors are returned, if the depth is 2, the target detail, its neighbours and neighbors of
    neighbors are returned and so on.

    :param details: A list of Detail objects representing the detail to search within.
    :param target_detail: The target detail for which neighboring detail are to be found.
    :param depth: The depth of neighbors to search.
    :return: A list containing all neighboring detail of the target detail up to the specified depth.
    """

    selected_details = {target_detail}
    for i in range(depth):
        current_details = selected_details.copy()
        for detail in current_details:
            selected_details.update(find_all_neighbours(details, detail))
    return list(selected_details)


def serialize_details_to_json(details: list[Detail], filename: str) -> None:
    """
    Serialize a list of Detail objects to a JSON file.

    :param details: List of Detail objects to be serialized.
    :param filename: The name of the JSON file to save the serialized data.
    """
    serialized_details = []
    for detail in details:
        serialized_detail = {
            "bottom_left": detail.bottom_left,
            "top_right": detail.top_right,
            "name": detail.name,
            "detail_type": detail.detail_type
        }
        serialized_details.append(serialized_detail)
    with open(filename, 'w') as file:
        json.dump(serialized_details, file, indent=4)


def deserialize_details_from_json(filename: str) -> list[Detail]:
    """
    Deserialize a list of Detail objects from a JSON file.

    :param filename: The name of the JSON file to deserialize.
    :return: List of Detail objects deserialized from the JSON file.
    """
    with open(filename, 'r') as file:
        serialized_details = json.load(file)
    details = []
    for serialized_detail in serialized_details:
        bottom_left = tuple(serialized_detail["bottom_left"])
        top_right = tuple(serialized_detail["top_right"])
        name = serialized_detail["name"]
        detail_type = serialized_detail["detail_type"]
        detail = Detail(bottom_left, top_right, name, detail_type)
        details.append(detail)
    return details


def count_detail_types(details: list[Detail]) -> dict[str, int]:
    """
    Count the number of each type of detail in the given list.
    This function takes a list of Detail objects and returns a dictionary
    where the keys are the types of details and the values are the counts
    of each type.

    :param details: A list of Detail objects to count.
    :return: A dictionary with detail types as keys and their respective counts as values.
    """

    detail_counts = {}
    for detail in details:
        if detail.detail_type in detail_counts:
            detail_counts[detail.detail_type] += 1
        else:
            detail_counts[detail.detail_type] = 1
    return detail_counts
