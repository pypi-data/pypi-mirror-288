# pylint: disable=C0103, C0115

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, confloat, conlist, conint


class RoadClass(str, Enum):
    motorway = "motorway"
    primary = "primary"
    secondary = "secondary"
    tertiary = "tertiary"
    residential = "residential"
    living_street = "living_street"
    trunk = "trunk"
    unclassified = "unclassified"
    parking_aisle = "parking_aisle"
    driveway = "driveway"
    alley = "alley"
    pedestrian = "pedestrian"
    footway = "footway"
    sidewalk = "sidewalk"
    crosswalk = "crosswalk"
    steps = "steps"
    path = "path"
    track = "track"
    cycleway = "cycleway"
    bridleway = "bridleway"
    unknown = "unknown"


class LaneDirection(str, Enum):
    forward = "forward"
    backward = "backward"
    both_ways = "both_ways"
    alternating = "alternating"
    reversible = "reversible"


class Heading(str, Enum):
    forward = "forward"
    backward = "backward"


class TravelMode(str, Enum):
    vehicle = "vehicle"
    motor_vehicle = "motor_vehicle"
    car = "car"
    truck = "truck"
    motorcycle = "motorcycle"
    foot = "foot"
    bicycle = "bicycle"
    bus = "bus"
    hgv = "hgv"
    hov = "hov"
    emergency = "emergency"


class RoadFlag(str, Enum):
    is_bridge = "is_bridge"
    is_link = "is_link"
    is_tunnel = "is_tunnel"
    is_under_construction = "is_under_construction"
    is_abandoned = "is_abandoned"
    is_covered = "is_covered"


class RoadSurface(str, Enum):
    unknown = "unknown"
    paved = "paved"
    unpaved = "unpaved"
    gravel = "gravel"
    dirt = "dirt"
    paving_stones = "paving_stones"
    metal = "metal"


class SpeedUnit(str, Enum):
    kmh = "km/h"
    mph = "mph"


class VehicleScope(str, Enum):
    axle_count = "axle_count"
    height = "height"
    length = "length"
    weight = "weight"
    width = "width"


class VehicleScopeComparison(str, Enum):
    greater_than = "greater_than"
    greater_than_equal = "greater_than_equal"
    equal = "equal"
    less_than = "less_than"
    less_than_equal = "less_than_equal"


class LinearlyReferencedPosition(BaseModel):
    position: confloat(ge=0, le=100)


class LinearlyReferencedRange(BaseModel):
    range: conlist(
        LinearlyReferencedPosition, min_length=2, max_length=2, unique_items=True
    )


class Speed(BaseModel):
    value: conint(ge=1, le=350)
    unit: SpeedUnit


class PurposeOfUse(str, Enum):
    as_customer = "as_customer"
    at_destination = "at_destination"
    to_deliver = "to_deliver"
    to_farm = "to_farm"
    for_forestry = "for_forestry"


class RecognizedStatus(str, Enum):
    as_permitted = "as_permitted"
    as_private = "as_private"
    as_disabled = "as_disabled"
    as_employee = "as_employee"
    as_student = "as_student"


class IntegerRelation(BaseModel):
    is_more_than: Optional[int] = None
    is_at_least: Optional[int] = None
    is_equal_to: Optional[int] = None
    is_at_most: Optional[int] = None
    is_less_than: Optional[int] = None


class LengthUnit(str, Enum):
    in_ = "in"
    ft = "ft"
    yd = "yd"
    mi = "mi"
    cm = "cm"
    m = "m"
    km = "km"


class LengthValueWithUnit(BaseModel):
    value: float = Field(ge=0)
    unit: LengthUnit


class LengthRelation(BaseModel):
    is_more_than: Optional[LengthValueWithUnit] = None
    is_at_least: Optional[LengthValueWithUnit] = None
    is_equal_to: Optional[LengthValueWithUnit] = None
    is_at_most: Optional[LengthValueWithUnit] = None
    is_less_than: Optional[LengthValueWithUnit] = None


class WeightUnit(str, Enum):
    oz_ = "oz"
    lb = "lb"
    st = "st"
    lt = "lt"
    g = "g"
    kg = "kg"
    t = "t"


class WeightValueWithUnit(BaseModel):
    value: float = Field(ge=0)
    unit: WeightUnit


class WeightRelation(BaseModel):
    is_more_than: Optional[WeightValueWithUnit] = None
    is_at_least: Optional[WeightValueWithUnit] = None
    is_equal_to: Optional[WeightValueWithUnit] = None
    is_at_most: Optional[WeightValueWithUnit] = None
    is_less_than: Optional[WeightValueWithUnit] = None


class Width(BaseModel):
    value: float = Field(gt=0)


class SequenceEntry(BaseModel):
    connector_id: str
    segment_id: str


class SegmentProperties(BaseModel):
    class_: Optional[RoadClass] = Field(None, alias="class")
    access_restrictions: Optional[dict] = None
    level: Optional[int] = None
    level_rules: Optional[dict] = None


class SegmentConditionalProperties(BaseModel):
    lanes: Optional[dict] = None
    prohibited_transitions: Optional[dict] = None
    road_surface: Optional[dict] = None
    road_flags: Optional[dict] = None
    speed_limits: Optional[dict] = None
    width_rules: Optional[dict] = None


class SegmentSubtype(str, Enum):
    road = "road"
    rail = "rail"
    water = "water"


class SegmentProps(BaseModel):
    subtype: SegmentSubtype
    connector_ids: List[str] = Field(default_factory=list)
    routes: Optional[List[dict]] = None
