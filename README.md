<a href="https://sandstormer.github.io/PokeRogue-Dex/">
  <img src="https://github.com/Sandstormer/PokeRogue-Dex/raw/main/ui/bigbutton.png">
</a>

## This repository is for the updater scripts for [Sandstorm's SearchDex](https://sandstormer.github.io/PokeRogue-Dex/). 

### 🔧 These scripts are only intended for use by developers.
The updater scripts read all the necessary data from the [game code](https://github.com/pagefaultgames/pokerogue/tree/main), process all the images, and put all the data into a compact format that is easily searchable for the SearchDex. I run these scripts whenever there is a game update. There is no need for anyone else to run these, unless I am unable to continue the project.
### ❌ This is <b>NOT</b> the repository for the SearchDex itself. 
If that is what you are looking for, you can go to [the website](https://sandstormer.github.io/PokeRogue-Dex/), or [see the source code](https://github.com/Sandstormer/PokeRogue-Dex).

## How to use

1. Install Python. I use Python 3.10.6, but other versions will probably work. Check your installed Python version with this command:

        python --version
   
2. Download or clone this repository. If you have Git installed, you can use the command:

        git clone https://github.com/Sandstormer/SearchDex-Updater.git

3. Run the following scripts in order, from an IDE. There are more instructions in each file.

- updateGameFiles.py
- updateImages.py
- updateDatabase.py
- updateFilters.py
- updateLangs.py

The website files for the [Searchdex itself](https://github.com/Sandstormer/PokeRogue-Dex) will be cloned into the "website" folder. If that folder already exists, that step will be skipped, and the website structure files (index.html, style.css, script.js) will not be updated. 

Running the update scripts will update the website data files such as pokedex_data.js, global_data.js, all {lang}.js, and all images. The website 'structure' mentioned above will not be modified.
