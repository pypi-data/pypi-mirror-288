from glom import glom

from calculations.types.enums.stroke_types import (
    STROKE_TYPES,
    STROKE_TYPES_FOR_150IM,
    STROKE_TYPES_FOR_200_400IM,
    STROKE_TYPES_FOR_MEDLEY,
)
from calculations.types.services.calculations.lane import LaneInformation
from calculations.utils.logging import Logger

logger = Logger()


def determine_stroke_type(index: int, lane_info: LaneInformation) -> str:
    stroke_type = glom(lane_info, "stroke_type", default="")
    distance = glom(lane_info, "lap_distance")
    pool_type = glom(lane_info, "pool_type", default="LCM")
    relay_leg = glom(lane_info, "relay_leg")
    relay_type = glom(lane_info, "relay_type", default=None)

    if stroke_type.lower() == STROKE_TYPES.MEDLEY.value.lower():
        possible_stroke_types = STROKE_TYPES_FOR_200_400IM

        # Medley race where stroke type determined by relay leg
        if relay_type != "" and relay_type != None:
            return STROKE_TYPES_FOR_MEDLEY[relay_leg]

        # Individual race where stroke type determined by annotation data index
        if pool_type == "LCM":
            refined_index = int((index - (index % 2)) / 2) if distance == 400 else index
        else:
            refined_index = (
                int((index - (index % 2)) / 4)
                if distance == 400
                else int((index - (index % 2)) / 2)
            )

        return possible_stroke_types[refined_index]

    # Para. Medley race where stroke type determined by relay leg
    if stroke_type.lower() == STROKE_TYPES.PARA_MEDLEY.value.lower():
        return STROKE_TYPES_FOR_150IM[relay_leg]

    return stroke_type
