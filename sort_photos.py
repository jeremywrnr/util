#!/usr/bin/env -S uv run python
import click
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def get_file_stats(folder, extensions):
    """
    Calculate the number of files and total size for given extensions.

    Returns: (count, total_size_bytes, files_by_extension)
    """
    folder_path = Path(folder)
    files_by_ext = defaultdict(list)
    total_size = 0
    count = 0

    # Convert extensions to set for faster lookup
    ext_set = {f".{ext.lower()}" for ext in extensions.split(',')}

    # Walk through directory recursively
    for file_path in folder_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ext_set:
            size = file_path.stat().st_size
            files_by_ext[file_path.suffix.lower()].append((file_path, size))
            total_size += size
            count += 1

    return count, total_size, files_by_ext

def format_size(bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

@click.command()
@click.option('-i', '--input-folder', required=True, type=click.Path(exists=True), help='Input folder containing media files')
@click.option('-o', '--output-folder', type=click.Path(), help='Output folder for sorted media files (omit for inline sorting)')
@click.option('--photo', is_flag=True, help='Process photos only')
@click.option('--video', is_flag=True, help='Process videos only')
@click.option('--move', is_flag=True, help='Actually move files (default is dry-run)')
@click.option('--inline', is_flag=True, help='Sort files inline (input and output are the same)')
@click.option('--force', is_flag=True, help='Skip confirmation prompt (automatically proceed)')
@click.option('--debug', is_flag=True, help='Enable debug output from photo_sort')
def sort_media(input_folder, output_folder, photo, video, move, inline, force, debug):
    """
    Sort photos and videos by date using photo_sort.

    By default, runs in DRY-RUN mode. Use --move to actually move files.
    Use --photo or --video flags to specify media type (if neither is specified, both are processed).
    Use --inline or omit -o/--output-folder to sort files in place.
    Use --force to skip confirmation prompt.
    """

    # Determine if we're doing inline sorting
    if inline and output_folder:
        click.echo("Error: Cannot specify both --inline and --output-folder.", err=True)
        sys.exit(1)

    temp_dir = None
    original_input = input_folder

    if not output_folder or inline:
        # Inline sorting: create temp directory in the SAME parent directory
        # This avoids cross-device link errors
        input_path = Path(input_folder)
        parent_dir = input_path.parent
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_dir = parent_dir / f"tmp_{input_path.name}_{timestamp}"
        temp_dir.mkdir(exist_ok=True)
        output_folder = str(temp_dir)
        is_inline = True
    else:
        is_inline = False

    # Determine which extensions to process
    photo_extensions = 'jpg,jpeg,png,gif,bmp,tiff,tif,heic,heif,raw,cr2,nef,arw,dng,orf,rw2'
    video_extensions = 'mp4,mov,avi,mpg,mpeg,m4v,wmv,flv,mkv,3gp,mts,m2ts,webm,vob,ogv'

    if photo and video:
        click.echo("Error: Cannot specify both --photo and --video flags. Choose one or neither (for both types).", err=True)
        sys.exit(1)

    if photo:
        extensions = photo_extensions
        media_type = "photos"
        video_ext_arg = ""  # Empty to disable videos
        photo_ext_arg = photo_extensions
    elif video:
        extensions = video_extensions
        media_type = "videos"
        video_ext_arg = video_extensions
        photo_ext_arg = ""  # Empty to disable photos - THIS IS THE FIX
    else:
        extensions = f"{photo_extensions},{video_extensions}"
        media_type = "photos and videos"
        video_ext_arg = video_extensions
        photo_ext_arg = photo_extensions

    # Get file statistics
    click.echo("Analyzing files...")
    file_count, total_size, files_by_ext = get_file_stats(input_folder, extensions)

    # Display summary
    click.echo(f"\n{'='*60}")
    click.echo(f"Input folder: {input_folder}")
    if is_inline:
        click.echo(f"Mode: INLINE SORTING (organizing in place)")
        click.echo(f"Temp folder: {output_folder}")
    else:
        click.echo(f"Output folder: {output_folder}")
    click.echo(f"Media type: {media_type}")
    click.echo(f"Operation: {'LIVE RUN (WILL MOVE FILES)' if move else 'DRY RUN (preview only)'}")
    click.echo(f"{'='*60}")
    click.echo(f"\nFiles to process: {file_count}")
    click.echo(f"Total size: {format_size(total_size)}")

    if files_by_ext:
        click.echo("\nBreakdown by extension:")
        for ext, files in sorted(files_by_ext.items()):
            ext_size = sum(size for _, size in files)
            click.echo(f"  {ext.upper():<6} {len(files):>5} files  ({format_size(ext_size)})")

    if file_count == 0:
        click.echo("\nNo files found matching the specified extensions.")
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)
        sys.exit(0)

    click.echo("")

    # Confirm before proceeding with live run (unless --force is set)
    if move and not force:
        warning = "⚠️  This will MOVE and REORGANIZE files"
        if is_inline:
            warning += " IN PLACE"
        warning += ". Continue?"
        if not click.confirm(warning):
            click.echo("Aborted.")
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir)
            sys.exit(0)

    # Build the command
    # For inline sorting, preserve original filenames
    if is_inline:
        file_format = '{date?%Y}/{original_filename}'
    else:
        file_format = '{date?%Y}/{date}_{original_name}{_:dup}.{ext?lower}'

    cmd = [
        'photo_sort',
        '--source-dir', input_folder,
        '--target-dir', output_folder,
        '--recursive',
        '--mkdir',
        '--date-format', '%Y-%m-%d_%H%M%S',
        '--file-format', file_format,
        '--nodate', 'NODATE/{original_filename}',
        '--move-mode', 'move',  # ALWAYS use move (fast)
        '--analysis-mode', 'exif_then_name',
        '--verbose'
    ]

    # Add debug flags if requested
    if debug:
        cmd.append('--debug')

    # Add photo and video extensions explicitly to avoid conflicts
    cmd.extend(['--extensions', photo_ext_arg])
    cmd.extend(['--video-extensions', video_ext_arg])

    # Always add dry-run unless --move is specified
    if not move:
        cmd.append('--dry-run')

    click.echo(f"\nRunning photo_sort...\n")

    # Execute the command
    try:
        result = subprocess.run(cmd, check=True)

        # If inline mode and successful, move files back
        if is_inline and move and result.returncode == 0:
            click.echo("\n" + "="*60)
            click.echo("Moving sorted files back to original location...")

            # Move everything from temp to original location
            for item in Path(output_folder).iterdir():
                dest = Path(original_input) / item.name
                if dest.exists():
                    # Remove old version
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                shutil.move(str(item), str(dest))

            click.echo(f"✓ Files successfully organized in place at {original_input}")

            # Clean up empty directories after moving files
            click.echo("\nCleaning up empty directories...")
            try:
                subprocess.run(
                    ['find', original_input, '-type', 'd', '-empty', '-delete'],
                    check=True,
                    capture_output=True
                )
                click.echo("✓ Empty directories removed")
            except subprocess.CalledProcessError:
                click.echo("⚠ Warning: Could not remove some empty directories", err=True)

        # Always clean up temp directory if it was created
        if temp_dir and Path(temp_dir).exists():
            click.echo("Cleaning up temporary directory...")
            shutil.rmtree(temp_dir)

        click.echo(f"\n{'='*60}")
        if move and not is_inline:
            click.echo("✓ Files successfully moved!")
        elif not move:
            click.echo("✓ Dry run completed. Use --move to actually move files.")
        click.echo(f"{'='*60}")
        sys.exit(result.returncode)

    except subprocess.CalledProcessError as e:
        click.echo(f"\nError: Command failed with exit code {e.returncode}", err=True)
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
        sys.exit(e.returncode)
    except FileNotFoundError:
        click.echo("\nError: 'photo_sort' command not found. Make sure it's installed and in your PATH.", err=True)
        click.echo("Install with: cargo install photo_sort")
        if temp_dir and temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user.")
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\nUnexpected error: {e}", err=True)
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
        sys.exit(1)

if __name__ == '__main__':
    sort_media()
