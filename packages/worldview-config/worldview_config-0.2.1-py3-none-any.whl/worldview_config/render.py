from collections import defaultdict
from pathlib import Path

import jinja2

from worldview_config import sub_paths, models

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates")
)

# Worldview has different names specifically in
# the measurements section
sat_names = {
    "aqua": "Aqua",
    "terra": "Terra",
    "snpp": "Suomi NPP",
    "noaa20": "NOAA-20",
    "noaa21": "NOAA-21",
}
sensor_names = {"CRIS": "CrIS"}


def render_layer(target: Path, layer: models.LayerConfig, filetype: str):
    if filetype == "metadata":
        subdir = "metadata"
        suffix = "md"
    elif filetype == "config":
        subdir = "wv.json"
        suffix = "json"
    else:
        raise ValueError("Unexpected layer type %s", filetype)

    layer_dir = Path(
        target,
        "common",
        "config",
        subdir,
        "layers",
        layer.instrument,
        layer.satellite,
    )
    layer_dir.mkdir(parents=True, exist_ok=True)
    layer_path = layer_dir / f"{layer.id}.{suffix}"
    tmpl = env.get_template(f"layer.{suffix}.jinja")
    lp = str(layer_path)
    tmpl.stream(layer=layer.model_dump()).dump(lp)
    if filetype == "metadata":
        tmpl.stream(layer=layer.model_dump()).dump(lp.replace(".md", ".html"))
    return


def render_layer_order(target: Path, layer_ids: list[str]):
    layer_order_path = target / sub_paths["layer_order"]
    tmpl = env.get_template("layerOrder.json.jinja")
    tmpl.stream(layer_ids=layer_ids).dump(str(layer_order_path))


def get_measurements(layers: models.LayerConfigs):
    mgroup = defaultdict(lambda: defaultdict(list))
    for layer in layers.root:
        sat = sat_names.get(layer.satellite, layer.satellite)
        sensor = layer.instrument.upper()
        sensor = sensor_names.get(sensor, sensor)
        source = f"{sat}/{sensor}"
        mgroup[layer.measurement][source].append(layer.id)
    return mgroup.items()


def render_measurement(target: Path, measurement: str, sources: dict):
    measurement_dir = target / sub_paths["measurements"]
    measurement_dir.mkdir(parents=True, exist_ok=True)
    measurement_path = measurement_dir / f"{measurement}.json"
    tmpl = env.get_template("measurement.json.jinja")
    tmpl.stream(name=measurement, sources=sources).dump(str(measurement_path))


def get_disciplines(layers: models.LayerConfigs):
    disciplines = defaultdict(list)
    for layer in layers.root:
        disciplines[layer.discipline].append(layer.measurement)
    return disciplines.items()


def render_discipline(target: Path, discipline: str, measurements: list[str]):
    discipline_dir = target / sub_paths["disciplines"]
    discipline_dir.mkdir(parents=True, exist_ok=True)
    discipline_path = discipline_dir / f"{discipline.capitalize()}.json"
    tmpl = env.get_template("discipline.json.jinja")
    tmpl.stream(discipline=discipline, measurements=measurements).dump(
        str(discipline_path)
    )


def render_templates(target: Path, layers: models.LayerConfigs):
    for layer in layers.root:
        render_layer(target, layer, "config")
        render_layer(target, layer, "metadata")

    render_layer_order(target, [layer.id for layer in layers.root])

    for measurement, sources in get_measurements(layers):
        render_measurement(target, measurement, sources)

    for discipline, measurements in get_disciplines(layers):
        render_discipline(target, discipline, measurements)
    return
