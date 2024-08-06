import os
import json
import shutil
from pathlib import Path

from worldview_config import sub_paths


def read_json(json_path: Path):
    with open(json_path) as f:
        out = json.load(f)
    return out


def merge_layer_order(target: dict, new: dict) -> dict:
    combined_layers = new["layerOrder"] + target["layerOrder"]
    combined_layers = list(set(combined_layers))
    return {"layerOrder": combined_layers}


def merge_measurement(target: dict, new: dict) -> dict:
    target = target["measurements"]
    new = new["measurements"]

    out = {"measurements": {}}
    ms = set(list(target) + list(new))
    for m in sorted(ms):
        if m in target:
            out["measurements"][m] = target[m]
        else:
            out["measurements"][m] = new[m]

        sources = set(list(target[m]["sources"]) + list(new[m]["sources"]))
        out["measurements"][m]["subtitle"] = ", ".join(sources)
        for source in sorted(sources):
            if m in target and m in new:
                if source in target[m]["sources"] and source in new[m]["sources"]:
                    out["measurements"][m]["sources"][source]["settings"] = list(
                        set(
                            target[m]["sources"][source]["settings"]
                            + new[m]["sources"][source]["settings"]
                        )
                    )
    return out


def merge_discipline(target: dict, new: dict) -> dict:
    out = target
    for d in sorted(out["categories"]["science disciplines"]):
        target_m = target["categories"]["science disciplines"][d]["measurements"]
        new_m = new["categories"]["science disciplines"][d]["measurements"]
        out["categories"]["science disciplines"][d]["measurements"] = sorted(
            list(set(target_m + new_m))
        )
    return out


def merge_json(target_path: Path, new_path: Path, category: str):
    target = read_json(target_path)
    new = read_json(new_path)
    match category:
        case "sources":
            target["sources"] |= new["sources"]
        case "features":
            target["features"] |= new["features"]
        case "layer_order":
            target = merge_layer_order(target, new)
        case "measurements":
            target = merge_measurement(target, new)
        case "disciplines":
            target = merge_discipline(target, new)
        case _:
            raise ValueError("Unsupported category %s", category)
    with open(target_path, "w") as f:
        json.dump(target, f)


def merge_config(target_root: Path, new_root: Path):
    for root, _, files in os.walk(new_root):
        for fname in files:
            new_path = Path(root, fname)
            target_path = Path(target_root, new_path.relative_to(new_root))
            target_path.parent.mkdir(exist_ok=True, parents=True)
            for category, subpath in sub_paths.items():
                if subpath in str(new_path):
                    if target_path.exists():
                        merge_json(target_path, new_path, category)
                    else:
                        new_path.rename(target_path)
                    break
            else:
                if target_path.exists():
                    shutil.move(new_path, target_path)
                else:
                    new_path.rename(target_path)
