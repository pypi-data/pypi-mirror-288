import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

from milgeo.builder import FeatureBuilder, PlacemarkBuilder
from milgeo.enum import PlatformType, ReliabilityCredibility


@dataclass
class Geometry:
    name: str
    coordinates: List
    metadata: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))

    id: Optional[str] = None
    sidc: Optional[str] = None
    observation_datetime: Optional[str] = None
    reliability_credibility: Optional[ReliabilityCredibility] = None
    staff_comments: Optional[str] = None
    platform_type: Optional[PlatformType] = None
    quantity: Optional[str] = None
    direction: Optional[str] = None
    speed: Optional[str] = None
    comments: Optional[str] = None
    outline_color: Optional[str] = None
    fill_color: Optional[str] = None
    fill_opacity: Optional[str] = None

    def __post_init__(self):
        if self.sidc and len(self.sidc) != 20:
            raise ValueError("sidc must be exactly 20 digits.")

        if self.platform_type and not isinstance(self.platform_type, PlatformType):
            raise ValueError("platform_type must be an instance of PlatformType.")

        if not self.coordinates:
            raise ValueError("coordinates cannot be empty.")

        if self.reliability_credibility and not isinstance(self.reliability_credibility, ReliabilityCredibility):
            raise ValueError(f"reliability_credibility '{self.reliability_credibility}' is not a valid ReliabilityCredibility value.")

        hex_color_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')

        if self.outline_color and not hex_color_pattern.match(self.outline_color):
            raise ValueError(f"outline_color '{self.outline_color}' is not a valid HEX color.")

        if self.fill_color:
            if not hex_color_pattern.match(self.fill_color):
                raise ValueError(f"fill_color '{self.fill_color}' is not a valid HEX color.")
            if not self.fill_opacity or not 0 <= float(self.fill_opacity) <= 1:
                raise ValueError(f"fill_opacity '{self.fill_opacity}' must be a number between 0 and 1 when fill_color is specified.")

        if self.observation_datetime:
            try:
                datetime.strptime(self.observation_datetime, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError(f"observation_datetime '{self.observation_datetime}' is not a valid timestamp in the format yyyy-MM-ddThh:mm:ss.")

        if self.quantity:
            try:
                int_quantity = int(self.quantity)
                if str(int_quantity) != self.quantity:
                    raise ValueError()
            except ValueError:
                raise ValueError(f"quantity '{self.quantity}' must be a string representing an integer.")

    @property
    def geometry_type(self):
        raise NotImplementedError("Subclasses should implement this property")

    @property
    def default_sidc(self):
        raise NotImplementedError("Subclasses should implement this property")

    def to_feature(self):
        builder = FeatureBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()

    def to_placemark(self):
        builder = PlacemarkBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()


@dataclass
class Point(Geometry):
    coordinates: List[float]

    @property
    def geometry_type(self):
        return "Point"

    @property
    def default_sidc(self):
        return "10012500001313000000"


@dataclass
class Line(Geometry):
    coordinates: List[List[float]]

    @property
    def geometry_type(self):
        return "LineString"

    @property
    def default_sidc(self):
        return "10016600001100000000"


@dataclass
class Polygon(Geometry):
    coordinates: List[List[List[float]]]

    @property
    def geometry_type(self):
        return "Polygon"

    @property
    def default_sidc(self):
        return "10012500001505010000"
