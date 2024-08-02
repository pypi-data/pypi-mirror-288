Python Package to extract information about the Stress, Strain and Young Modulus from a set of `.TRA` files

# Set up Instructions

Run the following command in the conda/miniconda terminal to install the package:
`pip install ciatta` 

Import the package in your Jupyter project or Python script:
`import ciatta`


# Available commands:
**Analyze a whole directory**
`ex.analyzeDirectory(folder_path, cut_off = True, sample_thickness = 10)` 
plots all the `.csv` files in the given directory. 


returns a pandas DataFrame containing 

Arguments:
- `folder_path` can be left empty to analyze the current working directory (e.g. `ciatta.analyzeDirectory()` )
- `folder_path` can be a relative path to a folder within the current working directory (e.g. `ciatta.analyzeDirectory('data')` )
- `folder_path` can be the absolute path (e.g. `ciatta.analyzeDirectory('C:\Users\Desktop\data')` )

# Mathematical Formulas


`Young Modulus` = slope of the best line fit for the curve

`Intercept` = the incercet of the previous fit

