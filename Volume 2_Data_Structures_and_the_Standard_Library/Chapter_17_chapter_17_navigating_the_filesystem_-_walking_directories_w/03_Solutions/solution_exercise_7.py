
#
# These sources are part of the "PyThon Programming Series" by Edgar Milvus, 
# you can find it on Amazon: https://www.amazon.com/dp/B0FTTQNXKG or
# https://tinyurl.com/PythonProgrammingSeries 
# New books info: https://linktr.ee/edgarmilvus 
#
# MIT License
# Copyright (c) 2025 Edgar Milvus
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Source File: solution_exercise_7.py
# Description: Solution for Exercise 7
# ==========================================

if __name__ == '__main__':
    try:
        START_PATH = setup_test_environment()
        
        # --- Run Exercise 1 ---
        print("\n" + "="*50)
        print("Running Exercise 1: File Type Inventory")
        counts = count_file_types(START_PATH)
        print("File Type Counts:", counts)
        # Expected: py=1, csv=1, txt=1, others=2 (md, bin)

        # --- Run Exercise 2 ---
        # Should skip .git, .venv, and node_modules
        pruned_paths = prune_traversal(START_PATH)
        
        # --- Run Exercise 3 ---
        total_bytes = get_total_size(START_PATH)
        human_size = format_bytes(total_bytes)
        print(f"Total size of all files: {total_bytes} bytes")
        print(f"Total size (Human readable): {human_size}")
        # Expected size should be slightly over 50 KB (due to large_data.bin)

        # --- Run Exercise 4 ---
        EXCLUSION_PATH_E4 = os.path.join(START_PATH, 'large_backups')
        
        # Note: We use the absolute path for exclusion
        found_files_e4 = advanced_file_finder(START_PATH, exclusion_paths=[EXCLUSION_PATH_E4])
        print(f"Total files found (excluding backups branch): {len(found_files_e4)}")
        print(f"Example found file: {found_files_e4[0]}")
        
        # --- Run Exercise 5 ---
        empty_dirs = find_empty_directories(START_PATH)
        print(f"Found {len(empty_dirs)} empty directories:")
        for d in empty_dirs:
            print(f"- {d}")
        # Expected: empty_folder and src/sub_empty
        
    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        
    finally:
        cleanup_test_environment()
        print("\n" + "="*50)
        print(f"Cleaned up test directory: {TEST_DIR}")
