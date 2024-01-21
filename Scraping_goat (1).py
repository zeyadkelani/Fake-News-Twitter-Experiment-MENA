from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import numpy as np
import time
import os

os.chdir(r'C:\Users\khale\Desktop\Twitter scraping') # change dir according to user
# List of URL suffixes
list_dates = pd.date_range(start="2023-09-01", end="2023-09-01", freq="D") # specify your date range 

def convert_date_standard_string(datelike_object):

    """
    Return string version of date in format mm/dd/yyyy

    Parameters
    -----------

    datelike_object
        A value of type date, datetime, or Timestamp.

        (e.g., Python datetime.datetime, datetime.date,
        Pandas Timestamp)

    """
    datelike_object= ["{:%d-%m-%Y}".format(i) for i in datelike_object]
    return datelike_object

#url_suffixes = convert_date_standard_string(list_dates)
url_suffixes=convert_date_standard_string(list_dates)
# Initialize an empty list to store the scraped data frames
data_frames = []

# Loop over the URL suffixes
for suffix in url_suffixes:
    url = f"https://archive.twitter-trending.com/egypt/{suffix}"
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(5) # change according to internet speed
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    hashtags = soup.findAll('span', attrs={'class': "word_ars"})
    numb_tweets = soup.findAll('tr', attrs={'class': "tr_table1"})

    hashtags = [tag.text for tag in hashtags]
    numb_tweets_1 = []
    class_1= []
    for tag in hashtags :
        if "#" in tag :
            class_1.append("Hashtags")
        else :
            class_1.append("Keywords")


    siblings=[]
    for tag in numb_tweets:
        sibling = tag.find('span',attrs={'class': "volume61"})
        if sibling != None :
            siblings.append(sibling.text.strip().replace('.', ','))
        else :
            siblings.append('0')
    tweetsc=[]
    for row in siblings:
        cleaned=row.replace(' tweet', '')
        tweetsc.append(cleaned)

    hashtags_df = pd.DataFrame({'Hashtags': hashtags})
    numb_tweets_df = pd.DataFrame({'Number of tweets': tweetsc})
    date_df = pd.DataFrame({'Date':np.repeat(suffix, len(hashtags_df), axis=0)})
    Keywords_df = pd.DataFrame({'Class': class_1})

    combined_df = pd.concat([hashtags_df, numb_tweets_df, date_df, Keywords_df], axis=1)
    data_frames.append(combined_df)

    driver.quit()  # Close the browser after each iteration

# Concatenate all the scraped data frames into one
result_df = pd.concat(data_frames, ignore_index=True)
# Print the combined result
print(result_df)
result_df.to_excel("Hashtags.xlsx")