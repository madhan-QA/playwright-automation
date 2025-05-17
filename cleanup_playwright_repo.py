import os
import shutil
import argparse
from pathlib import Path


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Clean up cache and temporary files from Playwright repository"
    )
    parser.add_argument(
        "--path", 
        default=".", 
        help="Path to the repository root (default: current directory)"
    )
    parser.add_argument(
        "--keep-logs", 
        action="store_true", 
        help="Keep log files (default: remove logs)"
    )
    parser.add_argument(
        "--keep-screenshots", 
        action="store_true", 
        help="Keep screenshot files (default: remove screenshots)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Show what would be deleted without actually deleting"
    )
    
    return parser.parse_args()


def get_size_str(size_bytes):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024 or unit == 'GB':
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024


def get_dir_size(path):
    """Calculate total size of a directory"""
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path) and not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


def remove_path(path, dry_run=False):
    """Remove a file or directory with proper error handling"""
    try:
        if os.path.exists(path):
            size = get_dir_size(path) if os.path.isdir(path) else os.path.getsize(path)
            size_str = get_size_str(size)
            
            if dry_run:
                print(f"Would remove: {path} ({size_str})")
                return size
            
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Removed directory: {path} ({size_str})")
            else:
                os.remove(path)
                print(f"Removed file: {path} ({size_str})")
            
            return size
    except Exception as e:
        print(f"Error removing {path}: {str(e)}")
    
    return 0


def find_files_to_clean(repo_path, keep_logs=False, keep_screenshots=False):
    """Find all files and directories to clean"""
    to_remove = []
    
    # Browser cache directories
    browser_cache_dirs = [
        ".cache/ms-playwright",  # Linux/macOS cache
        "Library/Caches/ms-playwright",  # macOS cache
        "AppData/Local/ms-playwright",  # Windows cache
    ]
    
    for cache_dir in browser_cache_dirs:
        full_path = os.path.join(os.path.expanduser("~"), cache_dir)
        if os.path.exists(full_path):
            to_remove.append(full_path)
    
    # Walk through repository to find Python cache and other files
    for root, dirs, files in os.walk(repo_path):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        # Find and mark __pycache__ directories
        if '__pycache__' in dirs:
            to_remove.append(os.path.join(root, '__pycache__'))
        
        # Find .pyc files outside __pycache__ directories
        for file in files:
            if file.endswith('.pyc'):
                to_remove.append(os.path.join(root, file))
                
            # Find trace files
            if file.endswith('.zip') and 'trace' in file:
                to_remove.append(os.path.join(root, file))
                
    # Handle screenshots directory
    screenshots_dir = os.path.join(repo_path, 'screenshots')
    if os.path.exists(screenshots_dir) and not keep_screenshots:
        to_remove.append(screenshots_dir)
        
    # Handle logs directory
    logs_dir = os.path.join(repo_path, 'logs')
    if os.path.exists(logs_dir) and not keep_logs:
        to_remove.append(logs_dir)
        
    return to_remove


def main():
    """Main function"""
    args = parse_arguments()
    repo_path = os.path.abspath(args.path)
    
    print(f"Scanning repository: {repo_path}")
    
    to_remove = find_files_to_clean(
        repo_path, 
        keep_logs=args.keep_logs,
        keep_screenshots=args.keep_screenshots
    )
    
    if not to_remove:
        print("No files to clean.")
        return
    
    print(f"\nFound {len(to_remove)} items to clean:")
    
    total_size_saved = 0
    for path in to_remove:
        size_saved = remove_path(path, args.dry_run)
        total_size_saved += size_saved
    
    action = "Would free" if args.dry_run else "Freed"
    print(f"\n{action} up {get_size_str(total_size_saved)} of disk space")
    
    if args.dry_run:
        print("\nThis was a dry run. No files were actually deleted.")
        print("Run again without --dry-run to perform the cleanup.")


if __name__ == "__main__":
    main()