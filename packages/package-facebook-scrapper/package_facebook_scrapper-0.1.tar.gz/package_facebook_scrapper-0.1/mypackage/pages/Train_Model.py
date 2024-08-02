import time
import streamlit as st
import config
import shutil
import os
from multiprocessing.dummy import Pool as ThreadPool
from facebook_scraping import FacebookScraping
from useful_function import accounts_split_in_sublists, create_true_false_csv
from random import choice
from time import sleep
from datetime import datetime
from classfication import train_and_save_ensemble_classifier
from PIL import Image


######################
# Page Title
######################
st.set_page_config(
    page_title="Facebook Detector",
    page_icon="logo.png",
)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.write("Here you can scrap Facebook accounts and train a Ramdom forest model")

image = Image.open('images/facebook-bots.jpg')
st.image(image, use_column_width=True)

st.write("""
# Fake Facebook accounts detector
Train a Random Forest Model with scrapped data from Facebook.
***
""")

######################

# True accounts list
st.header('Enter the Ture accounts in this format')

sequence_input = "5345453\ndfsf.jglksadjf\nsdjflas\n345353453\nrtljewjjt\n5345346\n43534654"

sequence = st.text_area("Please provide the True accounts that you wish to be scrapped.", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = ', '.join(sequence)  # Concatenates list to string

# Prints the input sequence
st.markdown('Used List for Scrapping:')
new_sequence = sequence.split(', ')
accounts_list_true = [int(item) if item.isdigit() else item for item in new_sequence]
st.text(list(accounts_list_true))

# dropbox menu - chose the number of posts to be scraped
num_posts = st.selectbox(
    'How many post would you like to scrap?',
    (1, 2, 3, 4, 5),
    index=3
)

st.write('You selected:', num_posts)

# dropbox menu chose the number of threads
num_threads = st.selectbox(
    "How many threads would you like to use (Be careful can't be more than the number of your CPUs)"
    "Additionally, the number of threads must match the number of accounts used for scraping.",
    (1, 2, 3, 4, 5),
    index=2
)

st.write('You selected:', num_threads)

# detect the progressbar
all_accounts_true = accounts_list_true.copy()

###################################################

DIRECTORY_NAME = "data"
NUM_OF_SPLITS = 3
NUMBER_OF_POSTS = num_posts + 1

used_fake_accounts = [
    [config.email_account1, config.password_account1],
    [config.email_account2, config.password_account2],
    [config.email_account3, config.password_account3]
]

pool = ThreadPool(num_threads)



# here are 3 functions for scrapping data, copy scraped file to data and process/read data to csv
#################################################################
def copy_to_data(DIRECTORY_NAME, FILE_NAME):
    if not os.path.exists(DIRECTORY_NAME):
        os.makedirs(DIRECTORY_NAME)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    destination_filename = f"{timestamp}_{FILE_NAME}"
    shutil.copy(FILE_NAME, os.path.join(DIRECTORY_NAME, destination_filename))


def scrapping(accounts_list: list, LABEL, FILE_NAME):
    facebook_scraping = FacebookScraping(all_accounts=accounts_list_true)
    fake_accounts = choice(used_fake_accounts)
    used_fake_accounts.remove(fake_accounts)
    l_driver = facebook_scraping.login(email=fake_accounts[0], password=fake_accounts[1])
    sleep(5)
    facebook_scraping.scrap_list_of_accounts_html(l_driver=l_driver,
                                                  list_of_accounts=accounts_list,
                                                  num_of_posts=NUMBER_OF_POSTS,
                                                  label=LABEL,
                                                  filename=FILE_NAME)

    return print("Threed is finished")

######################################################
# scrap true accounts
######################################################
true_json = "True_accounts_scraped.json"
true_sublists = accounts_split_in_sublists(all_accounts_true, NUM_OF_SPLITS)

if st.button('Scrap True accounts now'):
    progress_text = "Operation in progress. Please wait."

    my_bar = st.progress(0, text=progress_text)
    percent_complete = 0
    arg_list_ = [true_json, "True", true_json]
    arg_list = [(sublist, "True", true_json) for sublist in true_sublists]

    if os.path.exists(arg_list_[2]):
        # Delete the file
        os.remove(arg_list_[2])
        print(f"File: {arg_list_[2]} deleted successfully.")
    else:
        print(f"File: {arg_list_[2]} does not exist.")

    fb_scrapping = FacebookScraping(all_accounts_true)
    results = pool.starmap(scrapping, arg_list)
    pool.close()
    pool.join()
    copy_to_data(DIRECTORY_NAME, arg_list_[2])
    time.sleep(2)
    st.success('Done!')
############################################################
# header of false accounts
###########################################################

st.header('Enter the False accounts in this format')

sequence_input = "5345453\ndfsf.jglksadjf\nsdjflas\n345353453\nrtljewjjt\n5345346\n43534654"
sequence = st.text_area("Please provide the False accounts that you wish to be scrapped.", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = ', '.join(sequence)  # Concatenates list to string

# Prints the input sequence
st.markdown('Used List for Scrapping:')
new_sequence = sequence.split(', ')
accounts_list_false = [int(item) if item.isdigit() else item for item in new_sequence]
st.text(list(accounts_list_false))

all_accounts_false = accounts_list_false.copy()

#############################################################
# scrap false accounts
#############################################################

false_json = "False_accounts_scraped.json"
false_sublists = accounts_split_in_sublists(all_accounts_false, NUM_OF_SPLITS)


if st.button('Scrap False accounts now'):
    progress_text = "Operation in progress. Please wait."

    my_bar = st.progress(0, text=progress_text)
    percent_complete = 0
    arg_list_ = [false_sublists, "False", false_json]
    arg_list = [(sublist, "False", false_json) for sublist in false_sublists]

    if os.path.exists(arg_list_[2]):
        # Delete the file
        os.remove(arg_list_[2])
        print(f"File: {arg_list_[2]} deleted successfully.")
    else:
        print(f"File: {arg_list_[2]} does not exist.")

    fb_scrapping = FacebookScraping(all_accounts_false)
    results = pool.starmap(scrapping, arg_list)
    pool.close()
    pool.join()
    copy_to_data(DIRECTORY_NAME, arg_list_[2])
    time.sleep(2)
    st.success('Done!')


####################################################################
# precess data
####################################################################
path_csv = "model_train_accounts.csv"

st.header('Data processing')
if st.button('Process the data'):
    st.subheader('Display the csv data')
    data_csv = create_true_false_csv(true_json, false_json, path_csv)
    copy_to_data(DIRECTORY_NAME, path_csv)
    print(data_csv)
    st.session_state.data_csv = data_csv
    st.write(st.session_state.data_csv)


########################################################################
# Train the model
########################################################################
# model_path = "rf_model.pkl"
# Classifier selection on the main screen
st.header("Select Classifiers")
classifiers = ["Logistic Regression", "K-Nearest Neighbors", "Random Forest", "Decision Tree", "Gradient Boosting"]
selected_classifiers = st.multiselect("Choose classifiers for the ensemble", classifiers)

if st.button('check the data'):
    # mean_metric = train_and_save_ensemble_classifier(st.session_state.data_csv, model_path)
    # copy_to_data(DIRECTORY_NAME, model_path)
    # st.write(f"Mean of all metrics: {mean_metric:.4f}")

    if not selected_classifiers:
        st.error("Please select at least one classifier.")
    else:
        # Train the model and display results
        model_save_path = 'ensemble_classifier.pkl'
        results = train_and_save_ensemble_classifier(st.session_state.data_csv, model_save_path, selected_classifiers)
        copy_to_data(DIRECTORY_NAME, model_save_path)

        st.write(f"Accuracy: {results['accuracy']:.4f}")
        st.write(f"Precision: {results['precision']:.4f}")
        st.write(f"Recall: {results['recall']:.4f}")
        st.write(f"F1-score: {results['f1']:.4f}")
        st.write(f"ROC AUC: {results['roc_auc']:.4f}")
        st.write(f"Mean of all metrics: {results['mean_metrics']:.4f}")