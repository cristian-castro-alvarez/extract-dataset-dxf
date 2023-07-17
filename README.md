# Dataset from .DXF Layers
This script extracts the line information from a
.DXF file that contains lines in different layers.
To be used, please export the lines in '2007 Lines' from Rhino.

## Virtual Environment
To set a Conda virtual environment with the required dependencies in Windows:
```bash
conda create --name myenv --file requirements.txt
```

## Repository
1. [run_extract_datasets.py](run_extract_datasets.py): (To be ran in a virtual environment) Extracts mapping cell lines and creates a 'bbdd_celdas.csv' file with the start and end of each mapping cell.
2. [run_cross_datasets.py](run_cross_datasets.py): (To be ran in FLAC3D) Assigns a geological domain to each cell point, according to their position in 3D.