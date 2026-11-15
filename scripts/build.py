"""Build each theme: bases/<base>.json + sources/<id>/theme.json + sources/<id>/combo.py -> themes/<id>.json.

sources/<id>/theme.json:
  name, appearance   as in a T3 theme
  base               a file in bases/ (without .json)
  light              "dark": the light appearance reuses the dark roles (art themes need light text)
                     "base": use the base's own light variant
  colors             roles that override the base, for both appearances when light is "dark"
  variants.light     roles that override the light variant only
combo.py gets the theme folder and the merged theme (without css) as JSON, and writes combo.css.
"""
import json, subprocess, sys, tempfile
from pathlib import Path

LIMIT = 20000
root = Path(__file__).resolve().parent.parent

def build(src: Path) -> None:
    cfg = json.loads((src / "theme.json").read_text())
    base = json.loads((root / "bases" / f"{cfg['base']}.json").read_text())
    dark = {**base["colors"], **cfg.get("colors", {})}
    light_overrides = cfg.get("variants", {}).get("light", {})
    if cfg.get("light", "base") == "dark":
        light = {**dark, **light_overrides}
    else:
        light = {**base.get("variants", {}).get("light", base["colors"]), **light_overrides}
    theme = {
        "version": 1,
        "name": cfg["name"],
        "appearance": cfg.get("appearance", "dark"),
        "canvas": dark["canvas"],
        "accent": dark["accent"],
        "colors": dark,
        "variants": {"light": light},
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(theme, f)
    subprocess.run([sys.executable, "-I", str(src / "combo.py"), str(src), f.name], check=True, stdout=subprocess.DEVNULL)
    Path(f.name).unlink()
    theme["css"] = (src / "combo.css").read_text()
    if len(theme["css"]) > LIMIT:
        sys.exit(f"{src.name}: css is {len(theme['css'])} chars, over T3's {LIMIT} limit")
    out = root / "themes" / f"{src.name}.json"
    out.write_text(json.dumps(theme, indent=2))
    print(f"built {out.relative_to(root)} on {cfg['base']} ({len(theme['css'])} css chars)")

for src in sorted((root / "sources").glob("*/theme.json")):
    build(src.parent)
