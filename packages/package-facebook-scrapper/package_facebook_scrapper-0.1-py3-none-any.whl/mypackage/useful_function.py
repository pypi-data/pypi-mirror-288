import json
import pandas as pd
from data_processing import pipeline_processor
from datetime import datetime
import shutil
import os


# spilt the provided list in sublists
def accounts_split_in_sublists(input_list, num_splits):
    # Calculate the length of each sublist
    sublist_length = len(input_list) // num_splits
    remainder = len(input_list) % num_splits  # Calculate the remainder

    # Initialize an empty list to store the sublists
    sublists = []
    start = 0

    # Iterate over the input list, creating sublists
    for i in range(num_splits):
        if i < remainder:
            sublist = input_list[start:start + sublist_length + 1]
            start += sublist_length + 1
        else:
            sublist = input_list[start:start + sublist_length]
            start += sublist_length

        sublists.append(sublist)

    return sublists


# load the JSON data True and False to convert it to csv
def create_true_false_csv(true_json, false_json, true_false_csv):
    with open(true_json, "r") as f:
        data_t = json.load(f)
    processed_data_t = pipeline_processor.fit_transform(data_t)
    with open(false_json, "r") as f:
        data_f = json.load(f)
    processed_data_f = pipeline_processor.fit_transform(data_f)
    concatenated_data = pd.concat([processed_data_t, processed_data_f], axis=0)
    concatenated_data.to_csv(true_false_csv, index=False)
    return concatenated_data


# copy data with timestamp to a file
def copy_to_data(DIRECTORY_NAME, FILE_NAME):
    if not os.path.exists(DIRECTORY_NAME):
        os.makedirs(DIRECTORY_NAME)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    destination_filename = f"{timestamp}_{FILE_NAME}"
    shutil.copy(FILE_NAME, os.path.join(DIRECTORY_NAME, destination_filename))
