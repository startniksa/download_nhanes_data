# About the project

The National Health and Nutrition Examination Survey (NHANES) is a survey research program conducted by the National Center for Health Statistics (NCHS) to assess the health and nutritional status of adults and children in the United States, and to track changes over time. The survey combines interviews, physical examinations and laboratory tests.

This code can be used to quickly download the data you need. It saves the source files into a `data` subfolder and creates a file `nhanes.csv` with all the data.

The code is copied from https://zenodo.org/record/2440203#.YzX3I0pByXI and put conveniently into one file with small changes.
Shoutout to the original author - Christopher Kelly.
I found the code by first reading the article [An interpretable machine learning model of biological age](https://f1000research.com/articles/8-17/v1).

# Install

Execute:

```
virtualenv venv -p python3
. venv/local/bin/activate
pip install -r requirements.txt
```

# Use

```
python download_files.py
```

# Download more data

I added Vitamin D data. I had to go to the website and find the name of the files and columns for each survey.

For example, for 2015-2016, I went to https://wwwn.cdc.gov/Nchs/Nhanes/Search/variablelist.aspx?Component=Laboratory&Cycle=2015-2016

I decided to use "25-hydroxyvitamin D3 (nmol/L)". The file is called `VID_I`, the column is `LBXVD3MS`.

However, for 2001-2002, the measured variable is "Vitamin D (nmol/L)", the file is called `VID_B`, the column is `LBDVIDMS`.

For 1999-2000 there is vitamin D data, but the unit is ng/mL.

The lines which add the Vitamin D data are marked with `#newly added` in the code.

2022-10

I added "White Blood Cells" data. 

The files which are downloaded already contain the WBC data. We just needed to add the columns to the input_col_map

However, the 2001-2002 data contained two values for WBC: LB2WBCSI and LBXWBCSI. This resulted in two columns, the second one called WBC_y.
Therefore be careful which variable you actually need. There were two different values for the same patients.