# ===== This is the first script of the SearchDex Updater =====
# ===== It grabs the entire official repo of Pokerogue    =====

# Summary of all steps:
# Step 1 is to run this script
# Step 2 is to run updateImages.py
# Step 3 is to run updateDatabase.py
# Step 4 is to run updateFilters.py
# Step 5 is to run updateLangs.py
# Step 6 is to use GitHub Desktop to review changes to the SearchDex website data.
# Step 7 is to manually test the functionality of the SearchDex.
# Step 8 is to push the changes to the SearchDex GitHub.

# There is a built-in patch comparison in updateDatabase.py and updateFilters.py
# That makes it easy to see what has changed in the new data
# The new data is compared to trimmed_data_prev.json and proc_data_prev.json
# To re-base the comparison, you must manually replace the "_prev" files with the current data
# trimmed_data_prev_shvar.json should only be re-based right before adding new variants

# If you are optimizing or making changes to the update scripts,
# you should use Git to compare the output files, to make sure they are unchanged

# Using "beta" usually causes errors, due to PokeRogue developers rapidly changing the game's code
# You should only do that temporarily, to apply an update before it hits live

branchName="wiki-scraper" # Set this to "main" or "beta"

import subprocess, os

# Function to reset everything in the folder, or clone it from scratch
def clone_or_update(repo_url, repo_dest, branch_name=None, only_clone=False):
    if not os.path.exists(repo_dest): # If the repo folder doesn't exist, clone it
        print(f"\nCloning repository into {repo_dest}...")
        if branch_name:
            cmd = ["git", "clone", "--depth", "1", "-b", branch_name, "--shallow-submodules", "--recursive", repo_url, repo_dest]
        else:
            cmd = ["git", "clone", "--depth", "1", repo_url, repo_dest]
        subprocess.run(cmd, check=True)
        return
    if only_clone: # Show an error if the website files already exist (they are not allowed to update)
        print(f"\nSearchDex files already exist in {repo_dest} folder")
        print(f"SearchDex website files will not be overwritten...")
        return
    if not os.path.exists(os.path.join(repo_dest, ".git")): # If folder exists but isn't a git repo,
        print(f"Folder exists at {repo_dest}...")           # tell the user to delete that folder
        input("Can't continue without deleting that folder")
        return
    # Continue if the folder exists and is a git repo (there are no errors)
    print(f"\nResetting repository at {repo_dest}...")
    subprocess.run(["git", "-C", repo_dest, "fetch", "--depth", "1", "origin"], check=True)
    if branch_name:
        subprocess.run(["git", "-C", repo_dest, "fetch", "--depth", "1", "origin", branch_name], check=True)
        subprocess.run(["git", "-C", repo_dest, "checkout", "-B", branch_name, "FETCH_HEAD"], check=True)
    else:
        subprocess.run(["git", "-C", repo_dest, "reset", "--hard", "origin/HEAD"], check=True)
    # Clean any untracked files/directories
    subprocess.run(["git", "-C", repo_dest, "clean", "-fdx"], check=True)
    # Initialize and update submodules recursively, force any local changes to be discarded
    subprocess.run(["git", "-C", repo_dest, "submodule", "update", "--init", "--recursive", "--force", "--depth", "1"], check=True)

# Update the entire repo of game files from the selected branch
# clone_or_update(repo_url="https://github.com/pagefaultgames/pokerogue.git", repo_dest="game_files", branch_name=branchName)
clone_or_update(repo_url="https://github.com/fabske0/pokerogue.git", repo_dest="game_files", branch_name=branchName)

# Get the SearchDex Website files ONLY if you don't have them (if you do, they will not be updated/replaced)
clone_or_update(repo_url="https://github.com/Sandstormer/PokeRogue-Dex.git", repo_dest="website", only_clone=True)

subprocess.run(["pnpm", "--version"], check=True)
subprocess.run(["pnpm", "install"], cwd="game_files", check=True)
subprocess.run(["pnpm", "wiki-scrape", "--json"], cwd="game_files", check=True)

print('\n======= ALL DONE =======\n')