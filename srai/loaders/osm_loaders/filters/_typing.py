"""Module contains a dedicated type alias for OSM tags filter."""
from typing import Dict, List, Union, cast

from srai.utils.typing import is_expected_type

osm_tags_type = Dict[str, Union[List[str], str, bool]]

grouped_osm_tags_type = Dict[str, Dict[str, Union[List[str], str, bool]]]


def merge_grouped_osm_tags_type(grouped_filter: grouped_osm_tags_type) -> osm_tags_type:
    """
    Merge grouped osm tags filter into a base one.

    Function merges all filter categories into a single one for an OSM loader to use.

    Args:
        grouped_filter (grouped_osm_tags_type): Grouped filter to be merged into a single one.

    Returns:
        osm_tags_type: Merged filter.
    """
    if not is_expected_type(grouped_filter, grouped_osm_tags_type):
        raise ValueError(
            "Provided filter doesn't match required `grouped_osm_tags_type` definition."
        )

    result: osm_tags_type = {}
    for sub_filter in grouped_filter.values():
        for osm_tag_key, osm_tag_value in sub_filter.items():
            if osm_tag_key not in result:
                result[osm_tag_key] = []

            # If filter is already a positive boolean, skip
            if isinstance(result[osm_tag_key], bool) and result[osm_tag_key]:
                continue

            # Check bool
            if isinstance(osm_tag_value, bool) and osm_tag_value:
                result[osm_tag_key] = True
            # Check string
            elif isinstance(osm_tag_value, str) and osm_tag_value not in cast(
                List[str], result[osm_tag_key]
            ):
                cast(List[str], result[osm_tag_key]).append(osm_tag_value)
            # Check list
            elif isinstance(osm_tag_value, list):
                new_values = [
                    value
                    for value in osm_tag_value
                    if value not in cast(List[str], result[osm_tag_key])
                ]
                cast(List[str], result[osm_tag_key]).extend(new_values)

    return result