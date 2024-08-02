# Facebook Post Scraper App

This app leverages `streamlit` and `selenium` to scrape public Facebook posts from designated accounts. Multiprocessing enables scraping from multiple accounts concurrently.

### Key Features

Concurrent Scraping: Supports concurrent scraping from multiple Facebook accounts using multiprocessing, 
significantly speeding up the data collection process.

![facebook_scrapping](images/img_1.png)

**Important Note:** Ensure the number of threads does not exceed your CPU cores to avoid performance issues.

**Configurable Scraping:** Allows users to define the number of posts to scrape and the number of concurrent scraping threads through the app’s interface.

**Data Processing Pipeline:** Processes collected data through a pipeline to prepare it for analysis.

**Random Forest Model:** Utilizes the processed data to create a Random Forest model for predictions.

### Setup and Configuration:
`Prerequisites`
`Python 3.9` or higher
`streamlit`
`selenium`
`multiprocessing`
`pandas`
`sklearn`
`numpy`
`scikit-learn`
`scipy`
`webdriver-manager`
`matplotlib`



**Installation**

1- Clone the repository:

```
git clone https://github.com/yourusername/facebook-post-scraper.git
cd facebook-post-scraper
```

2- Install the required packages:

```
pip install -r requirements.txt
```

### Fake Accounts Setup

To use the app, you'll need to create at least two fake Facebook accounts. 
Configure these accounts in the `config.py` file as follows:

`````
email_account1 = "facebook@email.com"
password_account1 = "password"

email_account2 = "facebook@email.com"
password_account2 = "password"

email_account3 = "facebook@email.com"
password_account3 = "password"
`````

### Running the App

To run the app, execute the following command:
`````
streamlit run .\Scrap_and_predict_accounts.py
`````

### User Interface

The app features an intuitive interface with two sidebars:

Scrap and predict accounts: Select and configure accounts for prediction.
Training Model: Select and configure accounts for training.

![front_page](images/img.png)


### Visualization

- The app generates visualizations to compare data from fake and true accounts. 
- This includes plots that help in understanding the distribution and characteristics of the scraped data.

![data_plot](images/img_2.png)

### Usage Instructions

**1. Define Scraping Parameters:**

- Set the number of posts to scrape.
- Set the number of concurrent threads in the app’s sidebar.

**Run the Scraper:** 

- Initiate the scraping process by clicking the appropriate button.

### Capabilities of the App for Training Regression Models and Generating Metrics

The app is able to train many regression models including:

- Logistic Regression
- K-Nearest Neighbors
- Random Forest
- Decision Tree
- Gradient Boosting

It also creates metrics such as:

- Accuracy
- Precision
- Recall
- F1
- Roc_auc
- Mean_metrics

![metrics](images/img_3.png)


- **View Results:** 

- Once the scraping is complete, view the processed data and generated plots.


**Model Training:**

- The app will process the data through a pipeline and create a Random Forest model for prediction purposes.

### Final Notes
- Ensure you follow all guidelines and ethical considerations while scraping data from Facebook. 
- Use this tool responsibly and only for purposes that comply with Facebook's policies and legal requirements.
