# ===== This is the first script of the SearchDex Updater =====
# ===== It grabs the entire official repo of Pokerogue    =====

# Summary of all steps:
# Step 1 is to run this script
# Step 2 is to run updateImages.py
# Step 3 is to run updateDatabase.py
# Step 4 is to run updateFilters.py
# Step 5 is to run updateLangs.py
# Step 6 is to use GitHub to review changes to the SearchDex website data.
# Step 7 is to manually test the functionality of the SearchDex.
# Step 8 is to push the changes to the SearchDex GitHub.

branchName="main" # Set this to "main" or "beta"
# Using "beta" often causes errors, due to PokeRogue developers rapidly changing the game's code
# You should only do that temporarily, to apply an update before it hits live

import subprocess, os

# Function to reset everything in the folder, or clone it from scratch
def clone_or_update(repo_url, repo_dest, branch_name=None, only_clone=False):
    if os.path.exists(repo_dest):
        if only_clone:
            print(f"\nSearchDex files already exist at {repo_dest}")
            print(f"Those files will not be updated...")
        else:
            if os.path.exists(os.path.join(repo_dest, ".git")):
                print(f"\nResetting repository at {repo_dest}...")
                subprocess.run(["git", "-C", repo_dest, "fetch", "--depth", "1", "origin"], check=True)
                if branch_name:
                    subprocess.run(["git", "-C", repo_dest, "checkout", branch_name], check=True)
                    subprocess.run(["git", "-C", repo_dest, "reset", "--hard", f"origin/{branch_name}"], check=True)
                else:
                    subprocess.run(["git", "-C", repo_dest, "reset", "--hard", "origin/HEAD"], check=True)
                # Clean any untracked files/directories
                subprocess.run(["git", "-C", repo_dest, "clean", "-fdx"], check=True)
                # Initialize and update submodules recursively, force any local changes to be discarded
                subprocess.run(["git", "-C", repo_dest, "submodule", "update", "--init", "--recursive", "--force", "--depth", "1"], check=True)
            else:
                # If folder exists but isn't a git repo, ask the user to delete it
                print(f"Folder exists at {repo_dest}...")
                input("Can't continue without deleting that folder")
    else:
        print(f"\nCloning repository into {repo_dest}...")
        if branch_name:
            cmd = ["git", "clone", "--depth", "1", "-b", branch_name, "--shallow-submodules", "--recursive", repo_url, repo_dest]
        else:
            cmd = ["git", "clone", "--depth", "1", repo_url, repo_dest]
        subprocess.run(cmd, check=True)

# Main files
clone_or_update(
    repo_url="https://github.com/pagefaultgames/pokerogue.git",
    repo_dest="game_files",
    branch_name=branchName
)

# SearchDex Website files
# If you already have these, they will not be updated/replaced
clone_or_update(
    repo_url="https://github.com/Sandstormer/PokeRogue-Dex.git",
    repo_dest="website",
    only_clone=True
)

print('\n======= ALL DONE =======\n')