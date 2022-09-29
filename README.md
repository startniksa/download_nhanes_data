# About the project

The National Health and Nutrition Examination Survey (NHANES) is a survey research program conducted by the National Center for Health Statistics (NCHS) to assess the health and nutritional status of adults and children in the United States, and to track changes over time. The survey combines interviews, physical examinations and laboratory tests.

This code can be used to quickly download the data you need. The code is copied from https://zenodo.org/record/2440203#.YzX3I0pByXI and put conveniently into one file.
Shoutout to the original author - Christopher Kelly.
I found the code by first reading the article [An interpretable machine learning model of biological age](https://f1000research.com/articles/8-17/v1).

# Install

Execute:

```
virtualenv venv -p python3
. venv/local/bin/activate
pip install -r requirements.txt
```

# Download more data

I added Vitamin D data. I had to go to the website and find the name of the files and columns for each survey.

For example I went to https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2003 > Laboratory Data > Vitamin D

Found that the file is probably called `L06VID_C`. The columns in the files have different names, I don't know where to find them.
I had to wait until the code opens the particular file and see how the column is called there.

The lines which add the Vitamin D data are marked with `#newly added` in the code.