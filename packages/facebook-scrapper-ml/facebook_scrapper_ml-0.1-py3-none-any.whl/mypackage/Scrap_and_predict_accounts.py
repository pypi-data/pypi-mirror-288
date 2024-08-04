import joblib
import time
import json
import pandas as pd
import streamlit as st
import config
import shutil
import os
from multiprocessing.dummy import Pool as ThreadPool
from facebook_scraping import FacebookScraping
from useful_function import accounts_split_in_sublists
from random import choice
from time import sleep
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from data_processing import pipeline_processor
from classfication import load_model_and_compute_metrics, load_model_and_predict
from PIL import Image
import matplotlib.pyplot as plt

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

st.sidebar.write(
    "Here you can scrap Facebook Accounts and your pretrained Random forest model to predict if the accounts are True or Fake")

image = Image.open('images/facebook-bots.jpg')
st.image(image, use_column_width=True)

st.write("""
# Fake Facebook accounts detector

This app utilizes a pre-trained Random Forest model for detecting fake Facebook accounts!

The model employs three parameters to classify whether a Facebook account is authentic or fake: 

the **mean number of likes**, the **mean number of comments**, and the **mean number of shares**.

The model was trained using a dataset consisting of 70 accounts, comprising 50 labeled as 'True' and 20 labeled as 
'False'.

***
""")

######################
st.header("Find below  metrics for the model.")
model_save_path = "ensemble_classifier.pkl"
data = "model_train_accounts.csv"

if st.button("load metrics"):
    results = load_model_and_compute_metrics(model_save_path=model_save_path, data=data)
    st.write(f"Accuracy: {results['accuracy']:.4f}")
    st.write(f"Precision: {results['precision']:.4f}")
    st.write(f"Recall: {results['recall']:.4f}")
    st.write(f"F1-score: {results['f1']:.4f}")
    st.write(f"ROC AUC: {results['roc_auc']:.4f}")
    st.write(f"Mean of all metrics: {results['mean_metrics']:.4f}")

# st.sidebar.header
st.header('Enter accounts in this format')

sequence_input = "5345453\ndfsf.jglksadjf\nsdjflas\n345353453\nrtljewjjt\n5345346\n43534654"

sequence = st.text_area("Please provide the accounts you wish to predict.", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = ', '.join(sequence)  # Concatenates list to string

# Prints the input sequence
st.header('Used List for Scrapping')
new_sequence = sequence.split(', ')
accounts_list_printed = [int(item) if item.isdigit() else item for item in new_sequence]
st.text(list(accounts_list_printed))

# dropbox menu - chose the number of posts to be scraped
num_posts = st.selectbox(
    'How many post would you like to scrap?',
    (1, 2, 3, 4, 5),
    index=3
)

st.write('You selected:', num_posts)

# dropbox menu chose the number of threads
num_threads = st.selectbox(
    "How many threads would you like to use (Be careful can't be more than the number of your CPUs), "
    "Additionally, the number of threads must match the number of accounts used for scraping.",
    (1, 2, 3, 4, 5),
    index=2
)

st.write('You selected:', num_threads)

# detect the progressbar
all_accounts = accounts_list_printed.copy()

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
new_list = accounts_split_in_sublists(all_accounts, NUM_OF_SPLITS)
print(new_list)


def creat_pred_csv(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        data_json = json.load(f)
    processed_data_json = pipeline_processor.fit_transform(data_json)
    processed_data_json.to_csv("pre_accounts.csv", index=False)


def copy_to_data(DIRECTORY_NAME, FILE_NAME):
    if not os.path.exists(DIRECTORY_NAME):
        os.makedirs(DIRECTORY_NAME)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    destination_filename = f"{timestamp}_{FILE_NAME}"
    shutil.copy(FILE_NAME, os.path.join(DIRECTORY_NAME, destination_filename))


def scrapping(accounts_list: list, LABEL, FILE_NAME):
    facebook_scraping = FacebookScraping(all_accounts=accounts_list_printed)
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


count = 1
if st.button('Scrap now'):
    progress_text = "Operation in progress. Please wait."

    my_bar = st.progress(0, text=progress_text)
    percent_complete = 0
    arg_list_ = [new_list, "No_Label", "pre_accounts.json"]
    arg_list = [(sublist, "No_Label", "pre_accounts.json") for sublist in new_list]
    print(arg_list)

    if os.path.exists(arg_list_[2]):
        # Delete the file
        os.remove(arg_list_[2])
        print(f"File: {arg_list_[2]} deleted successfully.")
    else:
        print(f"File: {arg_list_[2]} does not exist.")

    fb_scrapping = FacebookScraping(all_accounts)
    results = pool.starmap(scrapping, arg_list)
    pool.close()
    pool.join()
    copy_to_data(DIRECTORY_NAME, arg_list_[2])
    creat_pred_csv(f"{arg_list_[2]}")
    time.sleep(2)
    st.success('Done!')

# Process the data
st.header('Data processing')
if st.button('Process the data'):
    st.subheader('Display the csv data')

    st.session_state.df = pd.read_csv("pre_accounts.csv")
    st.write(st.session_state.df)

st.header('Make predictions')
if st.button('check the data'):
    y_pred, y_pred_proba = load_model_and_predict(model_save_path, st.session_state.df)
    st.session_state.df["prdicted data"] = y_pred
    st.session_state.df.drop("label", axis=1, inplace=True)
    st.write(st.session_state.df)

# plot the result
st.header("plot the data")
if st.button("Plot the data"):
    labels = 'True', 'False'
    sizes = st.session_state.df["prdicted data"].value_counts()

    fig1, ax1 = plt.subplots()
    plt.style.use('dark_background')
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)
