<a href="https://sandstormer.github.io/PokeRogue-Dex/">
  <img src="https://github.com/Sandstormer/PokeRogue-Dex/raw/main/ui/bigbutton.png">
</a>

## This repository is for the updater scripts for [Sandstorm's SearchDex](https://sandstormer.github.io/PokeRogue-Dex/). 

### 🔧 These scripts are only intended for use by developers.
The updater scripts read all the necessary data from the [game code](https://github.com/pagefaultgames/pokerogue/tree/main), process all the images, and put all the data into a compact format that is easily searchable for the SearchDex. I run these scripts whenever there is a game update. There is no need for anyone else to run these, unless I am unable to continue the project.
### ❌ This is <b>NOT</b> the repository for the SearchDex itself. 
If that is what you are looking for, you can go to [the website](https://sandstormer.github.io/PokeRogue-Dex/), or [see the source code](https://github.com/Sandstormer/PokeRogue-Dex).

## How to use

1. Install [Python 3.10.6](https://www.python.org/downloads/release/python-3106/). Newer version may also work. You can check your installed Python version with this command:

        python --version

2. Install the following Python submodules, by executing this command:

        pip install numpy pillow

3. Install [Git](https://git-scm.com/download/win) for your operating system. This is necessary.
   
4. Clone this repository, by running the following command in a folder of your choice:

        git clone https://github.com/Sandstormer/SearchDex-Updater.git

5. Run the following scripts in order, from an IDE. There are more instructions in each file.

- updateGameFiles.py
- updateImages.py
- updateDatabase.py
- updateFilters.py
- updateLangs.py

The first script clones the repository of the game files. Also, the website files for the [SearchDex itself](https://github.com/Sandstormer/PokeRogue-Dex) will be cloned into the "website" folder. If the "website" folder already exists, that step will be skipped, and the website structure files (index.html, style.css, script.js) will not be updated. This allows the script to fetch new game files without overwriting changes I make to the website.

Running the update scripts will update the website data files such as pokedex_data.js, global_data.js, all {lang}.js, and all images. The website 'structure' mentioned above will not be modified.
