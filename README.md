# Sentiment Analysis of Financial Documents

This project focuses on performing sentiment analysis on financial documents, specifically the 10-K filings of companies in the DOW JONES index. The goal is to gain insights into the sentiment expressed in these documents and understand the relative sentiment for each company over time.

## Problem Statement
The financial industry heavily relies on information from company filings to make informed decisions. Analyzing the sentiment in these documents can provide valuable insights into market trends, investor sentiment, and potential risks. This project aims to develop a data pipeline and sentiment analysis model to automate the process of extracting sentiment from financial documents and provide a sentiment analysis over time for companies in the DOW JONES index.

## Data Collection
A data pipeline is built that scrapes data from the SEC's EDGAR system, specifically targeting the 10-K filings of companies in the DOW JONES index using BeautifulSoup. The pipeline retrieves the past 10 years' worth of 10-K documents for each company. By collecting this data, we ensure a comprehensive analysis of the sentiment expressed by these companies over time. We also focus on data cleaning - only  the relevant sections of the documents is extracted.

## Data Cleaning and Preprocessing
Once the 10-K documents are obtained, a rigorous data cleaning and preprocessing step is performed. NLP preprocessing techniques such as stopword removal, lemmatization, digit removal, and punctuation removal are applied to improve the quality of the text data.

## Data Analysis
To analyze the sentiment expressed in the financial documents, two different approaches are used: Bag of Words with Jaccard similarity and TF-IDF with cosine similarity. These methods help quantify the sentiment and compare it across different documents over time. The results obtained from each approach are then plotted to visualize the relative sentiment for each company over time. The results for the Apple stock is shown below:

![image](https://github.com/kedarghule/Sentiment-Analysis-of-Financial-Documents/assets/41315903/1a2a7014-9903-44de-a662-822dded1905f)
![image](https://github.com/kedarghule/Sentiment-Analysis-of-Financial-Documents/assets/41315903/e110d08f-4aa7-412a-bc77-0d9cb543a778)

## Sentiment Analysis
The state-of-the-art sentiment analysis model called FinBERT, provided by the HuggingFace transformers library, is utilized. This pretrained model is specifically designed for financial sentiment analysis on corporate documents. It assigns sentiment labels (positive, negative, or neutral) to each document, enabling a more accurate understanding of the sentiment expressed in the financial reports. This is utilized to find the sentiment of the 10-K filings of each company. The inference process is sped up using multiprocessing.

## Conclusion
By leveraging a data pipeline to collect, clean, preprocess, and analyze financial documents, this project enables sentiment analysis of companies in the DOW JONES index. The combination of traditional methods like Bag of Words and TF-IDF with the advanced FinBERT model allows for a comprehensive understanding of the sentiment expressed in these documents over time. The insights gained from this analysis can assist investors, analysts, and financial institutions in making informed decisions based on the sentiment of financial reports.
