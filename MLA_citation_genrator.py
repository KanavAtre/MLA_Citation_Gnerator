import streamlit as st
from bs4 import BeautifulSoup
import requests
import spacy
import pandas as pd
import json
import pandas as pd


dates = [] # the array to store all dates


# streamlit interface making

st.title("MLA Format Citation Generator")
url = st.text_area("Enter the website/article URL")
button = st.button("Generate APA Citation")

#Setting up Streamlit

if "en_core_web_sm" not in spacy.util.get_installed_models():
    spacy.cli.download("en_core_web_sm")


# loading up the nlp database
nlp = spacy.load("en_core_web_sm")

#Header declaration for scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}



#Inputting the url from user using header
if url:
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is not successful
        soup = BeautifulSoup(response.content, "html.parser")

    except requests.exceptions.RequestException as e:
        st.write("Error occurred while fetching the URL:", e)
        st.write("Enter a valid URL")
else:
    st.write("No URL provided.")

#Scraping the content from provided URL
if url:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")


def find_title_name():

    '''
    Sets us a html parser operation to find the title name
    :return: title of the article
    '''
    title = str(soup.find('title').contents[0])
    titles = title.split("|")
    title = titles[0]

    if title == "None" or title == '403 Forbidden':
        title = soup.title.get_text().strip() if soup.title else 'Unknown Title'

    return title


def find_publish_date():
    '''
    Uses nlp to find the publish date from given URL

    In case date does not exist, returns a date not found message

    :return: publish date of the article
    '''
    text = soup.get_text()
    gutten_nlp = nlp(text[:10000])
    final_date = "Date Not Found"

    for entity in gutten_nlp.ents:
        if entity.label == "DATE":
            st.write("HELLO")
            if ("published" or "Published") in text[:entity.end_char].strip():
                final_date = entity.text
                break
            else:
                dates.append(entity.text)
    return final_date

def find_author_name():

    '''
    uses nlp operations to access the name of the author

    :return: author name of the article
    '''

    author_name = "Author name not found"

    author_meta = soup.find("meta", {"name": "author"})
    # Extracting the author name if found
    if author_meta:
        author_name = author_meta.get("content")
    else:
        text = soup.get_text()
        gutten_nlp = nlp(text[:10000])

        for entity in gutten_nlp.ents:
            if entity.label == "PERSON":
                if text[:entity.end_char].strip().endswith('by'):
                    author_name = entity.text
                    break
                else:
                    author_name = "Author name not found"

    return author_name


def final_apa_format(date, title, author_name):

    last_name = author_name.strip()[1]
    first_name = author_name.strip()[0]

    pass
    #return last_name  + "," + first_name + "." +



if button:
    st.write("Title: " + find_title_name())
    st.write("Author: " + find_author_name())

    #final output formatting in streamlit

    if find_publish_date() != "Date Not Found":
        st.write(find_publish_date())
    else:
        st.write(dates)

    st.write(find_publish_date())

# animal = st.radio("What animal is your favourite?", ("Lions", "Tiger", "Jaguar"))
