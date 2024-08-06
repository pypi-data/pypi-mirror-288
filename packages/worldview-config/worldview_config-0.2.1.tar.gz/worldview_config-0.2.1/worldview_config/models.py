from datetime import datetime

from pydantic import BaseModel, Field, RootModel

class Projection(BaseModel):
    source: str
    matrixSet: str

class LayerConfig(BaseModel):
    id: str
    satellite: str
    instrument: str
    measurement: str
    discipline: str
    title: str
    format: str
    colormap_id: str
    projections: dict[str, Projection]
    start_date: datetime
    group: str = Field(default="overlays")
    description: str = Field(default="")
    tags: list[str] = Field(default=[])
    period: str | None = Field(default="daily")
    end_date: datetime | None = Field(default=None)
    temporal_start: datetime | None = Field(default=None)
    temporal_end: datetime | None = Field(default=None)
    date_interval: int | None = Field(default=None)


class LayerConfigs(RootModel):
    root: list[LayerConfig]
