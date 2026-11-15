# t3-themes

Custom T3 Code themes. Each theme is `themes/<id>.json`; T3 loads them from `~/.t3/userdata/themes/`.

## Changing a theme

1. Edit the source: CSS lives in `sources/<id>/combo.py`, color roles in `themes/<id>.json`.
2. Run `scripts/build.sh`. It writes the CSS into the theme JSON, checks T3's 20,000-character limit, and installs.
3. Apply it with `t3_theme_set` passing only `themeId`. The files carry the CSS, so the tool call stays small; a full `theme` payload drags ~11k characters of image data through the call and risks corrupting it.
4. Run `scripts/shot.sh` and look at the image before replying. Done when every screen in **Screens to check** looks right.

## Screens to check

- New thread: "What should we blast in …?" heading and composer at the bottom. `shot.sh` captures only what is on screen, so ask the user to open a new thread before this pass.
- Conversation with messages: text readable over the art.
- Question card: the composer turns into it while the agent waits for the user's input (`AskUserQuestion`). The question blocks your turn, so start `sleep 8; scripts/shot.sh` in the background first, then ask.
- Settings → Appearance.
- Both appearances, via `t3_theme_set` `appearance`: dark shows Spotlight, light shows Floor.

## Finding a selector

Start with the stable selectors listed by `t3_theme_read`, then the map below. For anything else, run `scripts/find-selector.sh '<attribute, class or visible text>'`; it unpacks the app bundle once per T3 version and prints the code around each match.

| Selector | What it is |
| --- | --- |
| `[data-chat-column]` | Wraps the chat header and chat area. Paint full-height backgrounds here, then make `[data-chat-header]` and `[data-workspace-area="conversation"]` transparent. |
| `[data-chat-column]:not(:has([data-timeline-row-kind]))` | An empty thread, i.e. the new-thread screen. |
| `[data-slot="sidebar-inner"]` | Sidebar surface. With `background-attachment: fixed` its art lines up with the chat column. |
| `[data-slot="composer-shell"]` | Composer wrapper. Its `::before` is the glass card, colored by the `surfaceRaised` role. |
| `[data-slot="composer-context-strip"]` | Row under the composer (checkout, branch, Full access). The app fills it with the canvas color. |
| `[class*="absolute inset-0 z-20 flex items-center"]` | New-thread overlay that centers the composer; the heading hangs above the composer. |
| `[class~="group/draft-hero"] h1` | New-thread heading; its first span holds "What should we build". |

The last two match Tailwind class strings, which change between T3 releases. After a T3 update, recheck them with `find-selector.sh`.

## Gotchas

- An image used in two places is embedded once as a `:root` custom property (`--im-pic`); embedding it twice breaks the 20,000-character limit.
- `sources/*/original.png` is the full-resolution source art and stays local (gitignored). `build.sh` needs only the committed `dith.webp`; re-dithering with `dither.py` needs the original.
