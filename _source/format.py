#!/usr/bin/env python3

import argparse
import re
import textwrap
from typing import List, Tuple

def wrap_text_with_border(
    input_file: str,
    output_file: str,
    width: int = 75,
    padding: int = 2,
    margin: int = 0
) -> None:
    """
    Reads text from input_file, formats it with proper line wrapping
    and writes it to output_file with a border design.

    Args:
        input_file: Path to the input file
        output_file: Path to the output file
        width: Total width of the document including borders and margin
        padding: Number of spaces to pad between text and border
        margin: Number of spaces to add outside the border
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Calculate adjusted width (total width minus margin)
    adjusted_width = width - (margin * 2)

    # Calculate text width (adjusted width minus borders and padding)
    text_width = adjusted_width - 2 - (padding * 2)

    # Process the content
    wrapped_lines = []

    # Process content line by line
    for line in content.split('\n'):
        # Empty lines
        if not line.strip():
            wrapped_lines.append('')
            continue

        # Determine indentation
        match = re.match(r'^(\s*)', line)
        initial_indent = match.group(1) if match else ""
        indent_len = len(initial_indent)

        # Subsequent lines should maintain the same indentation
        subsequent_indent = initial_indent

        # Adjust width for indentation
        adjusted_width = text_width - indent_len

        # Process lines with pattern repetition (// followed by characters)
        pattern_match = re.search(r'//(.+)$', line)
        if pattern_match:
            pattern = pattern_match.group(1)
            # Replace the // pattern with the actual pattern
            base_line = line.split('//')[0]
            # Calculate how many patterns can fit
            remaining_width = text_width - len(base_line)
            repeat_count = remaining_width // len(pattern)
            if repeat_count > 0:
                repeated_pattern = pattern * repeat_count
                # Truncate if necessary
                if len(repeated_pattern) > remaining_width:
                    repeated_pattern = repeated_pattern[:remaining_width]
                line = base_line + repeated_pattern
            else:
                line = base_line

        # Process lines with line markers (/ followed by a character)
        line_marker_match = re.match(r'^/(.)', line)
        line_marker = None
        if line_marker_match:
            line_marker = line_marker_match.group(1)
            print(f"Found line marker: {line_marker}")
            # Remove the marker from the line
            line = line[2:]
            print(f"Line after removing marker: '{line}'")
            # Add marker to the start
            line = line_marker + line[1:] if line else line_marker
            print(f"Line after adding marker to start: '{line}'")

        # If line is already shorter than the width, just add it
        if len(line) <= text_width:
            wrapped_lines.append(line)
            continue

        # Store the line marker for subsequent lines
        subsequent_line_marker = line_marker
        print(f"Subsequent line marker: {subsequent_line_marker}")

        # Special handling for bullet points and lists
        bullet_match = re.match(r'^\s*[•\-*]\s', line)
        print(f"Checking if line is a bullet point: '{line}'")
        print(f"Is bullet point: {bool(bullet_match)}")

        if bullet_match:
            # For list items, we want to indent continuation lines
            list_marker_match = re.match(r'^(\s*[•\-*]\s+)', line)
            if list_marker_match:
                list_marker = list_marker_match.group(1)
                subsequent_indent = ' ' * len(list_marker)
                # Remove the bullet point for wrapping
                text_to_wrap = line[len(list_marker):]
                # Adjust width to account for indentation
                adjusted_width = text_width - len(subsequent_indent)
                # Wrap the text
                wrapped_text = textwrap.fill(
                    text_to_wrap,
                    width=adjusted_width,
                    initial_indent='',
                    subsequent_indent=''
                )
                # Add back the indentation
                wrapped_parts = wrapped_text.split('\n')
                wrapped_lines.append(list_marker + wrapped_parts[0])
                for part in wrapped_parts[1:]:
                    if subsequent_line_marker:
                        print('line marker!')
                        # For bullet points, we need the marker plus proper indentation to align with text after bullet
                        # Format: indent + marker + spaces + bullet-continuation-indent + part

                        # Calculate how the bullet point first line is indented
                        bullet_line = wrapped_lines[-1]
                        bullet_match = re.match(r'^(\s*' + re.escape(subsequent_line_marker) + r'\s+[•\-*]\s+)', bullet_line)

                        if bullet_match:
                            # Get the full indentation pattern up to after the bullet
                            full_indent = bullet_match.group(1)
                            # Replace the bullet with spaces to get the continuation indentation
                            indent_pattern = re.sub(r'[•\-*]', ' ', full_indent)
                            wrapped_lines.append(indent_pattern + part)
                        else:
                            print("falling back!")
                            # Fallback - should not normally reach here
                            wrapped_lines.append(initial_indent + subsequent_line_marker + "   " + "  " + part)
                    else:
                        wrapped_lines.append(subsequent_indent + part)
                continue

        # Regular line wrapping
        # Remove initial indentation for wrapping
        text_to_wrap = line[indent_len:]
        wrapped_text = textwrap.fill(
            text_to_wrap,
            width=adjusted_width,
            initial_indent='',
            subsequent_indent=''
        )

        # Add back the indentation and line markers
        wrapped_parts = wrapped_text.split('\n')
        wrapped_lines.append(initial_indent + wrapped_parts[0])

        # For continuation lines, add line marker if present
        for part in wrapped_parts[1:]:
            if subsequent_line_marker:
                # Add marker with the same spacing pattern as the original line
                # Format should match the original first line with the marker
                match = re.match(r'^(\s*)' + re.escape(subsequent_line_marker) + r'(\s+)', wrapped_lines[-1])
                if match:
                    # Extract the exact spacing pattern used in the first line
                    pre_marker_space = match.group(1)
                    post_marker_space = match.group(2)
                    wrapped_lines.append(pre_marker_space + subsequent_line_marker + post_marker_space + part)
                else:
                    # Fallback to consistent spacing
                    wrapped_lines.append(subsequent_indent + subsequent_line_marker + "   " + part)
            else:
                wrapped_lines.append(subsequent_indent + part)

    # Format with border
    formatted_lines = format_with_border(wrapped_lines, width, padding, margin, output_file)

    # Write to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(formatted_lines))
        print(f"Successfully formatted resume and saved to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")


def format_with_border(lines: List[str], width: int, padding: int, margin: int, filename: str = "resume.txt") -> List[str]:
    """
    Add border design to the wrapped text.

    Args:
        lines: List of wrapped text lines
        width: Total width of the document
        padding: Number of spaces for padding
        margin: Number of spaces to add outside the border
        input_file: Name of the input file to display in header

    Returns:
        List of lines with border design
    """
    # Extract filename for the header
    filename = filename.split('/')[-1]

    # Calculate adjusted width (total width minus margin)
    adjusted_width = width - (margin * 2)

    # Create header with filename and utf-8 indicator
    header_text = f"── [{filename}] "
    # Calculate correct fill length to ensure alignment with exact width
    remaining_width = adjusted_width - len(header_text) - 14  # 12 = "┌" + " utf-8 ───┐"
    header_fill = '─' * remaining_width
    header = f"┌{header_text}{header_fill} [utf-8] ───┐"

    bottom_border = f"└{'─' * (adjusted_width - 2)}┘"

    # Apply margin to start of each line
    margin_spaces = ' ' * margin

    result = [margin_spaces + header]

    # Add empty line at the beginning
    result.append(margin_spaces + f"│{' ' * (adjusted_width - 2)}│")

    # Process each line
    for line in lines:
        # Calculate padding needed to fill width
        padding_needed = adjusted_width - 2 - len(line) - padding * 2
        if padding_needed < 0:
            padding_needed = 0
            line = line[:adjusted_width - 2 - padding * 2]

        # Format line with border and padding
        formatted_line = f"│{' ' * padding}{line}{' ' * (padding_needed + padding)}│"
        result.append(margin_spaces + formatted_line)

    # Add bottom border (no additional empty line at the end)
    result.append(margin_spaces + bottom_border + "\n")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Format resume with border design')
    parser.add_argument('input_file', help='Path to input resume file')
    parser.add_argument('output_file', help='Path to output formatted file')
    parser.add_argument('-w', '--width', type=int, default=75, help='Width of document (default: 75)')
    parser.add_argument('-p', '--padding', type=int, default=2, help='Padding between text and border (default: 2)')
    parser.add_argument('-m', '--margin', type=int, default=0, help='Margin around the outside of the border (default: 0)')

    args = parser.parse_args()

    wrap_text_with_border(
        args.input_file,
        args.output_file,
        args.width,
        args.padding,
        args.margin
    )
