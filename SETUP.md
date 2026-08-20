# How this profile README works

`README.md` embeds two SVGs via `<picture>`, so GitHub serves the dark one to
dark-mode visitors and the light one to everyone else.

## Files

| File | Purpose |
| --- | --- |
| `art.txt` | The ASCII portrait, 70 columns wide. Plain text — edit any character. |
| `build_svg.py` | Rebuilds both SVGs from `art.txt` + the panel content at the top of the file. |
| `today.py` | Queries the GitHub GraphQL API and rewrites only the numbers in the SVGs. Runs nightly. |
| `cache/` | Per-repo commit-count cache keyed by a hash of the username. Delete to force a full recount. |

## Required repository secrets

| Secret | Value |
| --- | --- |
| `USER_NAME` | `williamengbjerg` |
| `ACCESS_TOKEN` | A PAT with read access to followers, starring, contents, metadata and commit statuses, across **all** repositories. |

Without "all repositories" scope the line-of-code total silently comes out low.

## Changing the text

Edit `PANEL` / `CONTACT` in `build_svg.py`, then:

```sh
python3 build_svg.py
```

That resets the stat numbers to `0`; the next `today.py` run fills them back in.
To do it immediately:

```sh
pip install -r cache/requirements.txt
ACCESS_TOKEN=<token> USER_NAME=williamengbjerg python3 today.py
```

The first run walks every commit of every repo you own or contributed to and
takes several minutes. Later runs read `cache/` and finish in seconds.

## Changing the portrait

`art.txt` is just text — hand-edit it, or regenerate from a photo. Keep it at
70 columns; `ART_COLS` in `build_svg.py` must match, since the panel's x
position is derived from it.

## Credit

Adapted from [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant).
