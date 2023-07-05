import os
import pickle
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords

def get_cleaned_data(path):
    with open(path, 'rb') as handle:
        data_dict = pickle.load(handle)
    
    return data_dict

def lemmatize_words(words):
    """
    Lemmatize words 

    Parameters
    ----------
    words : list of str
        List of words

    Returns
    -------
    lemmatized_words : list of str
        List of lemmatized words
    """
    wnl = WordNetLemmatizer()
    lemmatized_words = [wnl.lemmatize(word, 'v') for word in words]
    
    return lemmatized_words

def lemmatize_data(data):
    word_pattern = re.compile('\w+')
    lemmatized_data = {}
    for company, datalst in data.items():
        lemmatized_data[company] = []
        for year, doc in datalst:
            doc = lemmatize_words(word_pattern.findall(doc))
            lemmatized_data[company].append((year, doc))
    return lemmatized_data

def remove_stopwords(data):
    preprocessed_data = {}
    lemma_english_stopwords = lemmatize_words(stopwords.words('english'))
    for company, datalst in data.items():
        preprocessed_data[company] = []
        for year, doc in datalst:
            doc = [word for word in doc if word not in lemma_english_stopwords]
            preprocessed_data[company].append((year, doc))
    return preprocessed_data

if __name__ == "__main__":
    nltk.download('wordnet')
    nltk.download('stopwords')
    path = './data/doc_dict.pickle'
    data = get_cleaned_data(path)
    print("Performing lemmatization....")
    data = lemmatize_data(data)
    print("Removing stopwords....")
    data = remove_stopwords(data)
    print("Data preprocessed successfully!")
    print("Writing cleaned data to pickle file....")
    with open('./data/pp_doc_dict.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('./data/pp_doc_dict.pickle', 'rb') as handle:
        b = pickle.load(handle)

    print("Pickle file and original dict match!" if data == b else "ERROR with pickle")