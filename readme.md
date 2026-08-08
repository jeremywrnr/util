utility scripts
===============

Personal command-line tools. This directory is on `$PATH`, so every file here is
a live command — adding a file adds a command, deleting one removes it.

git
---

| tool | what it does |
| --- | --- |
| `git-exec` | run a command in every git repo under the cwd — `git exec 'pwd && git up'` |
| `git-add-commit-push` | add all, commit, push to the current branch (aliased to `acp`) |
| `fcp` | same, but only for the files you name |
| `git-historian` | interactive rebase all the way back to the root commit |
| `git-remote-setter` | flip a repo's origin between https and ssh |
| `mirror-github.sh` | mirror a GitHub repo onto the self-hosted Gitea instance |

media
-----

| tool | what it does |
| --- | --- |
| `avi-to-mp4` | convert avi/mov/mkv/wmv/… to mp4, re-encoding only when needed |
| `mp4-to-gif` | mp4 → gif |
| `webp-to-gif` | animated webp → gif, frame by frame |
| `flac-to-mp3` | flac → mp3 via lame, carrying id3 tags over |
| `qta-to-mp3` | qta → mp3 |
| `upload-music.sh` | rsync an album to the NAS inbox for Lidarr to import |

images
------

| tool | what it does |
| --- | --- |
| `image-to-jpg` | bmp/gif → jpg (first frame for animated gifs) |
| `heic-to-jpg` | heic → jpg via sips |
| `jpg-to-png` | jpg/jpeg → png |
| `webp-to-png` | webp → png |
| `svg-to-png` | svg → png |
| `svg-to-pdf` | svg → pdf |
| `ai-to-svg` | Illustrator .ai → plain svg via Inkscape |
| `set-media-date` | write EXIF/metadata dates onto images and videos |
| `remove-rightslink-images` | strip RightsLink watermark bars out of downloaded pdfs |

files
-----

| tool | what it does |
| --- | --- |
| `rmds` | delete the `.DS_Store` files macOS leaves behind |
| `dudir` | recursive directory size and file-count listing |
| `count-extensions` | count files by extension, recursively |
| `dedupe-check` | dry-run duplicate scan (rdfind) |
| `dedupe-clean` | delete duplicates found by rdfind |

system
------

| tool | what it does |
| --- | --- |
| `net` | ping-loop until the connection comes back, reporting downtime |
| `ssl-status` | show the cert verification status for a host |
| `timesync.sh` | force macOS to resync the clock against Apple's NTP servers |
| `cw` | print the source of any script on `$PATH`, by name |
| `hw` | same, syntax-highlighted through pygmentize |

dotfiles
--------

| tool | what it does |
| --- | --- |
| `srcdot` | link (or `-c` copy, `-b` back up) `~/Code/dotfiles` into `$HOME` |
| `zshrc-update` | edit, commit, push, and relink the zshrc (aliased to `zshrc`) |
| `vimrc` | same, for the vim config |
