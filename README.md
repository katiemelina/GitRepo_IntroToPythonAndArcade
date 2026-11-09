# GitRepo_IntroToPythonAndArcade
Directory for Tribal GIS Layer Up Workshop Participants.

# Introduction to Python and Arcade: Data Cleaning, Visualization, and Sharing
**Instructor:** Katharine Williams, PhD
**Duration:** 2-Day Workshop

Welcome to the workshop repository! This space contains the notebooks, sample projects, messy datasets, and bonus scripts you'll need to move from raw data to scripted ArcGIS Pro workflows.

---

## 🚀 Quick Start: How to Get These Files

You don't need to be a Git master to use this repo. Choose whichever option feels easiest:

### Option A: The Easy Way (ZIP Download) - recommended for the in-person workshop
1. Click the green **`< > Code`** button at the top right of this page.
2. Select **Download ZIP**.
3. Unzip the folder directly onto your desktop or local workspace.

### Option B: Clone via VS Code / Git (if you're feeling adventurous)
You must have Git installed, or the VS Code Git extension. Open your terminal or VS Code and run:

```bash
git clone https://github.com/katiemelina/GitRepo_IntroToPythonAndArcade.git
```

(Note: If Wi-Fi acts up or downloads fail, your instructor also has these files ready on backup thumb drives in the room!)

---

## 📂 Repository Structure

```
├── 01_handouts/                  # Setup guide, syntax cheat sheet, course roadmap, key points
├── 02_notebooks/
│   ├── 01_helloworld.ipynb               # Notebook 1: Jupyter, Python basics, loading your first data
│   ├── 02_data_exploration.ipynb         # Notebook 2: Exploring a messy CSV with pandas
│   ├── 03_data_wrangling.ipynb           # Notebook 3: Cleaning data and building script tools
│   ├── 03b_historytopython.ipynb         # Notebook 3b: Turning geoprocessing history into Python
│   ├── 04_Arcade.ipynb                   # Notebook 4: Symbology, labels, and popups with Arcade
│   ├── 05_SharingAndAPIs.ipynb           # Notebook 5: ArcGIS Online and the iNaturalist API
│   ├── 05b_Challenge.ipynb               # Bonus: Capstone challenge
│   ├── 05b_Solutions.ipynb               # Bonus: Capstone solutions
│   ├── 06_BatchProcessing.ipynb          # Bonus: Batch processing
│   ├── 07_InteractiveMapDashboards.ipynb # Bonus: Interactive maps
│   ├── extra_ScriptToolset.ipynb         # Extra: A set of script tools
│   └── symbols/                          # Cartoon map symbols used in Notebook 4
├── 03_pro_project/
│   ├── IntroToPythonAndArcade.aprx       # ArcGIS Pro project
│   ├── IntroToPythonAndArcade.gdb        # Project geodatabase
│   └── *.atbx                            # Script toolboxes
├── 04_data/
│   └── raw/                              # Raw iNaturalist CSVs (roadrunners and coyotes)
└── 05_scripts/                           # Standalone Python scripts used by the script tools
```

The `working` and `clean` data folders are created automatically when you run the notebooks.

---

## 🛠️ Prerequisites Checklist

Before we dive in, make sure you have:

1. ArcGIS Pro installed and licensed.
2. VS Code installed with the Python and Jupyter extensions.
3. Your workspace pointed to the default arcgispro-py3 Python environment (see Handout #1 for step-by-step instructions).
