#!/usr/bin/env python3
"""
Pre-processor to split large Markdown files into Canvas-ready structure:
- Parts (# headers) become Canvas Modules (directories)
- Chapters (## headers) become Canvas Pages (individual .md files)
- index.org files created (flat structure only so far) to preserve ordering
"""

import os
import re
import argparse
from pathlib import Path

def sanitize_filename(text):
    """Convert text to Canvas-compatible filename (lowercase with hyphens)."""
    text = text.strip().lower()
    # Replace problematic characters and spaces with hyphens
    text = re.sub(r'[^\w\s-]', '', text)  # Remove special chars except word chars, spaces, hyphens
    text = re.sub(r'\s+', '-', text)      # Replace spaces with hyphens
    text = re.sub(r'-+', '-', text)       # Replace multiple hyphens with single hyphen
    return text.strip('-')

def sanitize_dirname(text):
    """Convert Part header to directory name."""
    # Extract "Part X: Name" and convert to "Part_X_Name"
    match = re.match(r'Part (\d+):\s*(.*)', text.strip())
    if match:
        part_num, part_name = match.groups()
        clean_name = sanitize_filename(part_name)
        return f"Part_{part_num}_{clean_name}"
    return sanitize_filename(text)

def split_course_content(input_file, output_dir):
    """Split the course markdown file into Parts (modules) and Chapters (pages).

    Parts (# headers) become Canvas Modules (directories)
    Chapters (## headers) become Canvas Pages (individual .md files)

    Args:
        input_file: Path to input markdown file
        output_dir: Output directory
    """

    output_path = Path(output_dir)
    content_path = output_path / "content" / "Modules"

    # Create base directories
    content_path.mkdir(parents=True, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_part = None
    current_chapter = None
    current_part_dir = None
    current_content = []
    front_matter = []
    in_front_matter = False
    front_matter_done = False
    in_code_block = False
    part_structure = {}  # Track structure for index.org files

    # Process front matter (YAML header)
    i = 0
    if lines and lines[0].strip() == '---':
        in_front_matter = True
        front_matter.append(lines[0])
        i = 1

        while i < len(lines):
            front_matter.append(lines[i])
            if lines[i].strip() == '---':
                front_matter_done = True
                i += 1
                break
            i += 1

    # Process remaining lines
    while i < len(lines):
        line = lines[i]

        # Track code blocks to avoid mistaking comments for headers
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        # Only check for headers when NOT in a code block
        if not in_code_block:
            # Check for Part header (# Part X:)
            if line.startswith('# Part ') and re.match(r'# Part \d+:', line):
                # Save previous chapter if exists
                if current_chapter and current_content and current_part_dir:
                    save_chapter(current_part_dir, current_chapter, current_content)
                    current_content = []

                # Start new part
                current_part = line[2:].strip()  # Remove "# "
                current_part_dir = content_path / sanitize_dirname(current_part)
                current_part_dir.mkdir(exist_ok=True)
                current_chapter = None
                part_structure[current_part] = []
                print(f"Creating part: {current_part_dir}")

            # Check for Chapter header (##)
            elif line.startswith('## '):
                # Save previous chapter if exists
                if current_chapter and current_content and current_part_dir:
                    save_chapter(current_part_dir, current_chapter, current_content)
                    current_content = []

                # Start new chapter
                current_chapter = line[3:].strip()  # Remove "## "
                current_content = []  # Don't include the header - we'll add YAML instead

                # Track chapter structure for index.org
                if current_part and current_part in part_structure:
                    part_structure[current_part].append(current_chapter)

            else:
                # Add line to current content
                if current_chapter:
                    current_content.append(line)
        else:
            # Add line to current content (we're in a code block)
            if current_chapter:
                current_content.append(line)

        i += 1

    # Save final chapter
    if current_chapter and current_content and current_part_dir:
        save_chapter(current_part_dir, current_chapter, current_content)

    # Create index.org files for each part
    create_index_files(content_path, part_structure)

def save_chapter(part_dir, chapter_name, content_lines):
    """Save a chapter as a markdown file with YAML header."""
    filename = sanitize_filename(chapter_name) + '.md'
    file_path = part_dir / filename

    print(f"  Creating chapter: {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        # Add YAML front matter with title
        f.write('---\n')
        f.write(f'title: {chapter_name}\n')
        f.write('---\n\n')

        # Write content (without the original ## header)
        f.writelines(content_lines)

def create_index_files(content_path, part_structure):
    """Create index.org files for each part listing actual .md files that exist."""
    for part_name, chapters in part_structure.items():
        part_dir = content_path / sanitize_dirname(part_name)
        index_path = part_dir / 'index.org'

        print(f"  Creating index: {index_path}")

        # Get list of actual .md files in this directory
        md_files = list(part_dir.glob('*.md'))
        md_filenames = [f.name for f in md_files]

        # Sort files by the order they appear in chapters list
        ordered_files = []
        for chapter_name in chapters:
            expected_filename = sanitize_filename(chapter_name) + '.md'
            if expected_filename in md_filenames:
                ordered_files.append(expected_filename)

        with open(index_path, 'w', encoding='utf-8') as f:
            for filename in ordered_files:
                f.write(f'- {filename}\n')

def main():
    """Main function to run the course splitter."""
    parser = argparse.ArgumentParser(
        description='Split large Markdown files into Canvas-ready structure (## headers become files)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s course.md                   # Split ## headers into files
  %(prog)s ../docs/course.md           # Specify different input file

Note: Currently only supports splitting at ## level (level 2).
Parts (# headers) become Canvas Modules, Chapters (## headers) become Pages.
        """
    )

    parser.add_argument(
        'input_file',
        help='Input Markdown file to split'
    )

    parser.add_argument(
        '--output', '-o',
        default='.',
        help='Output directory (default: %(default)s)'
    )

    args = parser.parse_args()

    # Resolve paths
    input_file = Path(args.input_file)
    output_dir = Path(args.output)

    if not input_file.exists():
        print(f"Error: {input_file} not found!")
        return 1

    print(f"Splitting {input_file} into Canvas module structure...")
    print(f"Split level: ## headers become individual files")
    print(f"Output directory: {output_dir}")

    split_course_content(input_file, output_dir)
    print("Done!")
    return 0

if __name__ == '__main__':
    exit(main())
