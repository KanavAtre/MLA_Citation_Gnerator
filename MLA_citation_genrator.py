import csv
import nltk
from nltk.corpus import stopwords
import streamlit as st
from bs4 import BeautifulSoup
import requests
import spacy
import pandas as pd
import json
import pandas as pd


nltk.download('stopwords')

dates = [] # the array to store all dates


# streamlit interface making


#st.title("MLA Format Citation Generator")

st.markdown("<h1 style='text-align: center;'>MLA Format Citation Generator</h1>", unsafe_allow_html=True)

url = st.text_area("Enter the website/article URL below")

# Create two columns
col1, col2 = st.columns([2, 1])

# Button in the first column
with col1:
    button = st.button("Generate APA Citation")

# Button in the second column
with col2:
    st.write("")  # Adding empty space for alignment
    button2 = st.button("Semantic Analysis")

#Setting up Streamlit

if "en_core_web_sm" not in spacy.util.get_installed_models():
    spacy.cli.download("en_core_web_lg")


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

    if button or button2:
        st.write("Please enter a URL to begin")

#Scraping the content from provided URL
if url:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")



def make_csv_file():

    if url:
        text = soup.get_text()

        with open("new_file.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Split the text into lines and write each line as a separate row in the CSV file
            for line in text.split('\n'):
                csvwriter.writerow([line])


def most_appearing_keyword():
    text = soup.get_text()
    appearing_words = {}
    final_words = []

    # Split text into words and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in text.split() if word.lower() not in stop_words]

    for word in words:
        if word not in appearing_words:
            appearing_words[word] = 1
        else:
            appearing_words[word] += 1

    appearing_words = sorted(appearing_words.items(), key=lambda item: item[1], reverse=True)

    count = 0

    for k, v in appearing_words:
        if count < 3 and k not in stop_words:  # Filter out stopwords
            final_words.append(k)
            count += 1

    return final_words

def appearence_numbers():
    text = soup.get_text()
    appearing_words = {}
    final_words = []

    # Split text into words and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in text.split() if word.lower() not in stop_words]

    for word in words:
        if word not in appearing_words:
            appearing_words[word] = 1
        else:
            appearing_words[word] += 1

    appearing_words = sorted(appearing_words.items(), key=lambda item: item[1], reverse=True)

    count = 0

    for k, v in appearing_words:
        if count < 3 and k not in stop_words:  # Filter out stopwords
            final_words.append(str(v))
            count += 1

    return final_words

def find_title_name():

    '''
    Sets us a html parser operation to find the title name
    :return: title of the article
    '''

    if url:
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

    if url:
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


    if url:
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

    if url:

        make_csv_file()
        title = st.text_input("Title", str(find_title_name().lower()))
        #st.write(find_title_name().lower(), title)
        author = st.text_input("Author", find_author_name().lower())
        date = st.text_input("Publish Date", find_publish_date().lower())
        #st.write(find_author_name().lower(), author)

        #final output formatting in streamlit

if button2:

    if url:
        word = ""
        words = most_appearing_keyword()
        appearences = appearence_numbers()

        st.write("1." + words[0] + ": " + appearences[0] + " appearences")
        st.write("2." + words[1] + ": " + appearences[1] + " appearences")
        st.write("3." + words[2] + ": " + appearences[2] + " appearences")

# animal = st.radio("What animal is your favourite?", ("Lions", "Tiger", "Jaguar"))