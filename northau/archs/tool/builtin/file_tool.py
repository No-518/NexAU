"""File operation tools for reading, editing, and searching files."""

import os
import re
import glob
from pathlib import Path
from typing import Dict, Any, Optional, List


def file_read(
    file_path: str,
    start_line: Optional[int] = None,
    end_line: Optional[int] = None,
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """
    Read file contents with optional line range.
    
    Args:
        file_path: Path to the file to read
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (1-indexed)
        encoding: File encoding
    
    Returns:
        Dict containing file contents and metadata
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                "status": "error",
                "error": f"File not found: {file_path}"
            }
        
        with open(path, 'r', encoding=encoding) as f:
            lines = f.readlines()
        
        # Apply line range if specified
        if start_line is not None or end_line is not None:
            start_idx = (start_line - 1) if start_line else 0
            end_idx = end_line if end_line else len(lines)
            lines = lines[start_idx:end_idx]
        
        # Add line numbers
        numbered_lines = []
        line_offset = start_line or 1
        for i, line in enumerate(lines):
            numbered_lines.append(f"{line_offset + i:4d}→{line.rstrip()}")
        
        return {
            "status": "success",
            "content": "\n".join(numbered_lines),
            "file_path": str(path.absolute()),
            "total_lines": len(lines),
            "encoding": encoding
        }
        
    except UnicodeDecodeError as e:
        return {
            "status": "error",
            "error": f"Encoding error: {e}",
            "file_path": file_path
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "file_path": file_path
        }


def file_edit(
    file_path: str,
    old_string: str,
    new_string: str,
    replace_all: bool = False
) -> Dict[str, Any]:
    """
    Edit a file by replacing text.
    
    Args:
        file_path: Path to the file to edit
        old_string: Text to replace
        new_string: Replacement text
        replace_all: Replace all occurrences (default: only first)
    
    Returns:
        Dict containing edit results
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                "status": "error",
                "error": f"File not found: {file_path}"
            }
        
        # Read file
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if old_string exists
        if old_string not in content:
            return {
                "status": "error",
                "error": f"String not found in file: '{old_string}'"
            }
        
        # Perform replacement
        if replace_all:
            new_content = content.replace(old_string, new_string)
            replacements = content.count(old_string)
        else:
            # Check if old_string appears multiple times
            count = content.count(old_string)
            if count > 1:
                return {
                    "status": "error",
                    "error": f"String appears {count} times in file. Use replace_all=True or provide more context."
                }
            new_content = content.replace(old_string, new_string, 1)
            replacements = 1
        
        # Write back to file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            "status": "success",
            "message": f"Successfully replaced {replacements} occurrence(s)",
            "file_path": str(path.absolute()),
            "replacements": replacements
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "file_path": file_path
        }


def file_search(
    pattern: str,
    path: str = ".",
    file_pattern: str = "*",
    recursive: bool = True,
    case_sensitive: bool = True,
    max_results: int = 100
) -> Dict[str, Any]:
    """
    Search for text patterns in files.
    
    Args:
        pattern: Regular expression pattern to search for
        path: Directory to search in
        file_pattern: File name pattern (glob)
        recursive: Search subdirectories
        case_sensitive: Case sensitive search
        max_results: Maximum number of results to return
    
    Returns:
        Dict containing search results
    """
    try:
        search_path = Path(path)
        if not search_path.exists():
            return {
                "status": "error",
                "error": f"Path not found: {path}"
            }
        
        # Compile regex pattern
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            return {
                "status": "error",
                "error": f"Invalid regex pattern: {e}"
            }
        
        # Find files to search
        if recursive:
            file_paths = search_path.rglob(file_pattern)
        else:
            file_paths = search_path.glob(file_pattern)
        
        results = []
        files_searched = 0
        
        for file_path in file_paths:
            if not file_path.is_file():
                continue
                
            if len(results) >= max_results:
                break
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                files_searched += 1
                
                for line_num, line in enumerate(lines, 1):
                    matches = regex.finditer(line)
                    for match in matches:
                        if len(results) >= max_results:
                            break
                            
                        results.append({
                            "file": str(file_path.relative_to(search_path)),
                            "line_number": line_num,
                            "line_content": line.rstrip(),
                            "match": match.group(),
                            "match_start": match.start(),
                            "match_end": match.end()
                        })
                        
            except (UnicodeDecodeError, PermissionError):
                # Skip files that can't be read
                continue
        
        return {
            "status": "success",
            "results": results,
            "total_matches": len(results),
            "files_searched": files_searched,
            "pattern": pattern,
            "search_path": str(search_path.absolute()),
            "truncated": len(results) >= max_results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "pattern": pattern,
            "path": path
        }