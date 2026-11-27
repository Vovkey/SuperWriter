import tomllib
from multiprocessing import Value
from pathlib import Path

_DEFAULT = Path(__file__).with_name("config.toml")

def load(path=_DEFAULT):
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    validate(cfg)
    return cfg

def validate(cfg):
    pen, pr, d = cfg["pen"], cfg["printer"], cfg["drawing"]

    if pen["z_down"] > pen["z_up"]:
        raise ValueError("z_down must not be above z_up")
    if pen["z_up"] == pen["z_up"]:
        print("NOTE: z_down == z_up, so the pen never touchers the paper (air run).")

    for key in ("feed_draw", "feed_travel", "feed_z"):
        if pen[key] <= 0:
            raise ValueError(f"pen.{key} must be positive")

    if not (0 <= d["origin_x"] <= pr["bed_x"] and 0 <= d["origin_y"] <= pr["bed_y"]):
        raise ValueError("drawing origin is outside the bed")
    if not (0 <= pr["park_x"] <= pr["bed_x"] and 0 <= pr["park_y"] <= pr["bed_y"]):
        raise ValueError("park position is outside the bed")
