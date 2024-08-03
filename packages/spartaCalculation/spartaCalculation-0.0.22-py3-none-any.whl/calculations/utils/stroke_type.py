from glom import glom

from calculations.types.enums.stroke_types import (
    STROKE_TYPES,
    STROKE_TYPES_FOR_150IM,
    STROKE_TYPES_FOR_200_400IM,
    STROKE_TYPES_FOR_MEDLEY,
)
from calculations.types.enums.ams_property import (
    RELAY_TYPE,
)
from calculations.types.services.calculations.lane import LaneInformation
from calculations.utils.logging import Logger

logger = Logger()


def get_relay_type(relay_type, distance):

    if relay_type == "4x100m" and int(distance) == 100:
        return None

    if relay_type == "4x50m" and int(distance) == 50:
        return None

    if relay_type == "4x200m" and int(distance) == 200:
        return None

    return relay_type


def determine_stroke_type(index: int, lane_info: LaneInformation) -> str:
    stroke_type = glom(lane_info, "stroke_type", default="")
    distance = glom(lane_info, "lap_distance")
    pool_type = glom(lane_info, "pool_type", default="LCM")
    relay_leg = glom(lane_info, "relay_leg")
    relay_type = get_relay_type(
        relay_type=glom(lane_info, "relay_type", default=None),
        distance=glom(lane_info, "lap_distance"),
    )

    if relay_type != "" and relay_type != None:
        relay_type_lowercase = relay_type.lower()

        if relay_type_lowercase in [
            RELAY_TYPE.FREESTYLE_RELAY.value.lower(),
            RELAY_TYPE.MIXED_FREESTYLE_RELAY.value.lower(),
        ]:
            return STROKE_TYPES.FREESTYLE.value

        if relay_leg != None:
            return STROKE_TYPES_FOR_MEDLEY[relay_leg]

    if stroke_type.lower() == STROKE_TYPES.MEDLEY.value.lower():
        return STROKE_TYPES_FOR_MEDLEY[index]

    if stroke_type.lower() in STROKE_TYPES.INDIVIDUAL_MEDLEY.value.lower():
        if pool_type == "LCM":
            refined_index = int((index - (index % 2)) / 2) if distance == 400 else index
        else:
            refined_index = (
                int((index - (index % 2)) / 4)
                if distance == 400
                else int((index - (index % 2)) / 2)
            )

        return STROKE_TYPES_FOR_200_400IM[refined_index]

    if stroke_type.lower() == STROKE_TYPES.PARA_MEDLEY.value.lower():
        return STROKE_TYPES_FOR_150IM[index]

    return stroke_type
