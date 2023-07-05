import re
from bs4 import BeautifulSoup
import pickle
import os
from get_data import get_ticker_data


def get_documents(text):
    """
    Extract the documents from the text

    Parameters
    ----------
    text : str
        The text with the document strings inside

    Returns
    -------
    extracted_docs : list of str
        The document strings found in `text`
    """
    # TODO: Implement
    final_docs = []
    start_regex = re.compile(r'<DOCUMENT>')
    end_regex = re.compile(r'</DOCUMENT>')
    
    start_idx = [x.end() for x in re.finditer(start_regex, text)]
    end_idx = [x.start() for x in re.finditer(end_regex, text)]
    
    for start_i, end_i in zip(start_idx, end_idx):
        final_docs.append(text[start_i:end_i])
    
    
    return final_docs

def get_document_type(doc):
    """
    Return the document type lowercased

    Parameters
    ----------
    doc : str
        The document string

    Returns
    -------
    doc_type : str
        The document type lowercased
    """
    # Regex explaination : Here I am tryng to do a positive lookbehind
    # (?<=a)b (positive lookbehind) matches the b (and only the b) in cab, but does not match bed or debt.
    # More reference : https://www.regular-expressions.info/lookaround.html
    
    type_regex = re.compile(r'(?<=<TYPE>)\w+[^\n]+') # gives out \w
    type_idx = re.search(type_regex, doc).group(0).lower()
    return type_idx

def remove_html_tags(text):
    """Remove HTML tags from the text"""
    text = BeautifulSoup(text, 'html.parser').get_text()
    return text


def clean_text(text):
    """Function to clean the text: convert to lower case and remove HTML tags"""
    text = text.lower()
    text = remove_html_tags(text)
    return text

if __name__ == "__main__":
    os.chdir("./data/sec-edgar-filings/")

    tickers = get_ticker_data() # Get the data

    link_dict = {}
    doc_dict ={}

    # Get doc_dict = {company: [(year, documents)]}
    for c in tickers:
        if c in os.listdir("./"):
            link_dict[c] = os.listdir(f"./{c}/10-K/")
            print(f"Getting documents for {c}")
            doc_dict[c] = []
            for i in link_dict[c]:
                if i:
                    file_path = f"./{c}/10-K/{i}/full-submission.txt"
                    with open(file_path, "r") as file:
                        data = file.read()
                    cik, year, val = i.split('-')
                    doc_dict[c].append((int("20"+year), data))

    # Get doc_dict2 = {company: [(year, [document1, document2, ..])]}
    doc_dict2 = {}
    for company, datalst in doc_dict.items():
        doc_dict2[company] = []
        for year, data in datalst:
            print(f"Arranging documents for {company} in {year}...")
            doc_dict2[company].append((year, get_documents(data)))  

    # Get final_doc_dict = {company: [(year, 10-k)]}
    final_doc_dict = {}
    for company, datalst in doc_dict2.items():
        final_doc_dict[company] = []
        for year, doclst in datalst:
            for doc in doclst:
                if get_document_type(doc) == '10-k':
                    print(f"Getting 10-k forms for {company} in {year}..")
                    final_doc_dict[company].append((year, clean_text(doc)))

    os.chdir("../")
    print("Writing cleaned data to pickle file....")
    with open('doc_dict.pickle', 'wb') as handle:
        pickle.dump(final_doc_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('doc_dict.pickle', 'rb') as handle:
        b = pickle.load(handle)

    print("Pickle file and original dict match!" if final_doc_dict == b else "ERROR with pickle")
