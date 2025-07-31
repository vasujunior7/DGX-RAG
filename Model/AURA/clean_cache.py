"""
Utility script to clean all cached files and force fresh generation
"""

import os
from pathlib import Path

def clean_cache():
    """Remove all cached preprocessing files"""
    files_to_remove = [
        "chunks.pkl",
        "faiss.index", 
        "answers.json",
        "session_data.json",
        "demo_session.json",
        "demo_session_fresh.json",
        "test_session.json"
    ]
    
    removed_count = 0
    for file_path in files_to_remove:
        if Path(file_path).exists():
            os.remove(file_path)
            print(f"🗑️ Removed: {file_path}")
            removed_count += 1
        else:
            print(f"⏭️ Not found: {file_path}")
    
    print(f"\n✅ Cleanup complete! Removed {removed_count} files.")
    print("Next run will create fresh chunks and index.")

if __name__ == "__main__":
    print("🧹 Cleaning cached files...")
    clean_cache()
