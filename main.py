import argparse
import glob
import os

from src.reader import FormCSV
from src.visualizer import display_cumulative

if __name__ == "__main__":
    # Find the CSV files
    pattern = "FORM_*.csv"
    data_dir = "/home/brian/dev/Just-Keep-Parsing/data"
    files = sorted(glob.glob(os.path.join(data_dir, pattern)))
    
    # Parse the CSV files
    form_dict = {}
    for filename in files:
        with open(filename) as f:
            form = FormCSV(filename)
            if form.description_df["Activity Variant"][0] == "pool":
                form_dict[os.path.basename(filename)] = form

    display_cumulative(form_dict, "temp.png")