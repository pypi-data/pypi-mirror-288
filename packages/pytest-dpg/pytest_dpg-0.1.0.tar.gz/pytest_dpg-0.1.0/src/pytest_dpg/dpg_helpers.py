from collections import defaultdict
from enum import StrEnum

import dearpygui.dearpygui as dpg


class DPGItem(StrEnum):
    BUTTON = "mvAppItemType::mvButton"
    GROUP = "mvAppItemType::mvGroup"
    TAB = "mvAppItemType::mvTab"
    SLIDER = "mvAppItemType::mvSliderInt"


def get_window_position() -> tuple[int, int]:
    return dpg.get_viewport_pos()


def get_item_min_position(item: int) -> tuple[int, int]:
    x, y = dpg.get_item_rect_min(item)
    return x + 1, y + 1


def get_item_max_position(item: int) -> tuple[int, int]:
    x, y = dpg.get_item_rect_max(item)
    return x - 1, y - 1


def get_item_value(item: int) -> int:
    return dpg.get_value(item)


def get_item_value_boundaries(item: int) -> tuple[int, int]:
    item_config = dpg.get_item_configuration(item)
    return item_config["min_value"], item_config["max_value"]


def get_items_dict() -> dict[str, list]:
    items = defaultdict(list)
    for item in dpg.get_all_items():
        item_type = dpg.get_item_type(item)
        items[item_type].append(item)

    return items


def get_item_children(item: int) -> list:
    dic = dpg.get_item_children(item)
    return sum(dic.values(), [])


def get_item_with_or_near_text(item_type: DPGItem, text: str) -> int:
    """
    Efficiently loop through items searching for matches.
    """
    matching_types = []
    indirect_matches = []

    for item in dpg.get_all_items():
        current_type = dpg.get_item_type(item)
        current_label = dpg.get_item_label(item)
        current_value = dpg.get_value(item)

        if current_type == item_type and current_label == text:
            # Direct match found
            return item

        if current_type == item_type:
            # Potential direct match (in case text is found later)
            matching_types.append(item)

        if text in [current_label, current_value]:
            indirect_matches.append(item)

    if matching_types and indirect_matches:
        for item in indirect_matches:
            parent = dpg.get_item_parent(item)
            for child in get_item_children(parent):
                if child in matching_types:
                    return child

    raise KeyError(
        f"Unable to find '{item_type}' with text '{text}' directly or indirectly"
    )


def get_item_center_position(item: int) -> tuple[int, int]:
    window_x, window_y = get_window_position()
    min_x, min_y = get_item_min_position(item)
    max_x, max_y = get_item_max_position(item)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    target_x = int(window_x + center_x)
    target_y = int(window_y + center_y)

    return target_x, target_y


def get_slider_position(item: int, value: int) -> tuple[int, int]:
    """Calculates the position of a slider handle given its item ID and a value.

    Args:
        item: The ID of the slider item.
        value: The value for which to calculate the position.

    Returns:
        A tuple of (x, y) coordinates representing the position of the slider handle.
    """

    window_x, window_y = get_window_position()
    min_x, min_y = get_item_min_position(item)
    max_x, max_y = get_item_max_position(item)

    # Apply offset
    min_x += 5
    min_y += 5
    max_x -= 5
    max_y -= 5

    min_val, max_val = get_item_value_boundaries(item)

    # Calculate the slider's length and the position of the given value relative to the min and max values
    slider_length = max_x - min_x
    value_range = max_val - min_val
    value_position = (value - min_val) / value_range

    # Calculate the x position of the slider handle
    handle_x = min_x + (slider_length * value_position)

    # Assuming the slider handle is centered vertically within the slider
    handle_y = (min_y + max_y) / 2

    # Convert to screen coordinates
    target_x = int(round(window_x + handle_x))
    target_y = int(round(window_y + handle_y))

    return target_x, target_y
