import argparse
import subprocess
import os

def get_all_branches():
    result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
    branches = result.stdout.strip().split('\n')
    return [branch.strip('* ') for branch in branches]

def get_current_branch():
    result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
    return result.stdout.strip()

def merge_branches(prefix):
    current_branch = get_current_branch()
    all_branches = get_all_branches()
    
    branches_to_merge = []
    if prefix == '*':
        branches_to_merge = [b for b in all_branches if b != current_branch]
    else:
        branches_to_merge = [b for b in all_branches if b.startswith(prefix) and b != current_branch]
    
    for branch in branches_to_merge:
        print(f"Merging branch: {branch}")
        result = subprocess.run(['git', 'merge', branch], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error merging {branch}:")
            print(result.stderr)
        else:
            print(f"Successfully merged {branch}")

def entry():
    parser = argparse.ArgumentParser(description="Merge Git branches with a given prefix.")
    parser.add_argument('prefix', help="Prefix of branches to merge. Use '*' to merge all branches.")
    args = parser.parse_args()

    if not os.path.exists('.git'):
        print("Error: Not a git repository")
        return

    merge_branches(args.prefix)