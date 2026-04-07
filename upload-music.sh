#!/bin/sh
# Upload music to NAS inbox for Lidarr to import
# Usage: ./upload-music.sh /path/to/album [/path/to/another]

if [ $# -eq 0 ]; then
    echo "Usage: upload-music.sh <path> [<path> ...]"
    exit 1
fi

for src in "$@"; do
    echo "Uploading: $src"
    rsync -avP "$src" nas:/volume2/Media/Downloads/
done

echo "Done. Check Lidarr (Wanted → Manual Import) to organize, then Navidrome will pick it up."

