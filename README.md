# t3-themes

Custom themes for T3 Code.

| Folder | What's in it |
| --- | --- |
| `themes/` | Installed themes. `scripts/install.sh` copies these into `~/.t3/userdata/themes/`. |
| `archive/` | Retired themes, kept for reference: Steel Ball Run and the Iron Dots Glass / Floor / Spotlight variants. Not installed. |
| `sources/` | Source art and the scripts that build each theme's background. |

## Iron Dots

Dotted Iron Man background (art: Art Roman, 2020), 256×144 dot grid with a 12-colour ordered dither.

- Dark appearance: **Spotlight** — light pool on the face, rest near-black.
- Light appearance: **Floor** — art fully lit, dark band rising from the bottom.

To change it, edit `sources/iron-dots/combo.py`, run `scripts/build.sh`, and re-select the theme in T3. `AGENTS.md` has the full loop, the screens to check, and the selectors that work.

`sources/iron-dots/original.png` (the source art) is not in the repo. To re-dither from it, put a copy there, then:

```sh
python3 -m venv .venv && .venv/bin/pip install pillow numpy   # also needs cwebp (Homebrew)
.venv/bin/python sources/iron-dots/dither.py sources/iron-dots/original.png sources/iron-dots 256 12 56
```

## Giorno

Giorno Giovanna on Whirl's base (`#131313` canvas and Whirl's dark colour roles, by saltjsx). Only Giorno is dotted: a darkened 400×225 square-dot dither, with the art's purple background cut out to flat canvas. The sidebar is plain. Both appearances use Whirl's dark roles, because light text has to sit on the dark art.

- Dark appearance: **Spotlight**.
- Light appearance: **Floor**.

Source art `sources/giorno/original.png` stays local. To re-dither (args: cols, colours, dither spread, brightness):

```sh
.venv/bin/python sources/giorno/dither.py sources/giorno/original.png sources/giorno 400 10 95 0.44
```
