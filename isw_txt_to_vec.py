import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from num2words import num2words


from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


import os
import pickle
import numpy as np


def remove_first_line(doc):
    first_line_end = doc.find('\n')
    doc = doc[first_line_end+1:]
    first_line_end = doc.find('\n')
    if doc[first_line_end-2] == 'E' and doc[first_line_end-1] == 'T':
        doc = doc[first_line_end + 1:]
    return doc


def convert_lower_case(doc):
    return np.char.lower(doc)


def remove_punctuation(doc):
    symbols = string.punctuation.replace(',', '') + '—\n’“”'
    for i in range(len(symbols)):
        doc = np.char.replace(doc, symbols[i], ' ')
        doc = np.char.replace(doc, "  ", " ")
    doc = np.char.replace(doc, ',', '')
    return doc


def remove_apostrophe(doc):
    return np.char.replace(doc, '-', '')


def convert_numbers(doc):
    tokens = word_tokenize(str(doc))
    new_doc = ""
    for w in tokens:
        if w.isdigit():
            if int(w) < 100000000000:
                w = num2words(w)
            else:
                w = ''
        new_doc += " " + w
    new_doc = np.char.replace(new_doc, '-', ' ')
    return new_doc


def remove_stop_words(doc):
    stop_words = set(stopwords.words('english'))
    not_stop_words = {'no', 'not'}
    stop_words -= not_stop_words
    tokens = word_tokenize(str(doc))
    new_doc = ""
    for w in tokens:
        if w not in stop_words and len(w) > 1:
            new_doc += " " + w
    return new_doc


def stem(doc):
    stemmer = PorterStemmer()
    tokens = word_tokenize(str(doc))
    new_doc = ""
    for w in tokens:
        new_doc += " " + stemmer.stem(w)
    return new_doc



def lemmatize(doc):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(str(doc))
    lemmatized_doc = ""
    for w in tokens:
        lemmatized_doc += " " + lemmatizer.lemmatize(w)
    return lemmatized_doc


def preprocess_document(doc, words_to_roots=stem):
    doc = remove_first_line(doc)
    doc = convert_lower_case(doc)
    doc = remove_punctuation(doc)
    doc = remove_apostrophe(doc)
    doc = convert_numbers(doc)
    doc = remove_punctuation(doc)
    doc = remove_stop_words(doc)
    doc = words_to_roots(doc)
    return doc


def preprocess_docs(directory, words_to_roots=stem):
    docs = list()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f, 'r', encoding='utf-8') as file:
            doc = file.read()
            docs.append(preprocess_document(doc, words_to_roots))
    return docs


def save_pickle(obj, path, filename, flag):
    with open(f"{path}/{filename}", flag) as handle:
        pickle.dump(obj, handle)


def write_document(doc, directory, name):
    f = open(f'{directory}/{name}', 'w', encoding='utf-8')
    f.write(doc)
    f.close()


def documents_to_vec(docs):
    cv = CountVectorizer(max_df=0.98, min_df=2)
    word_count_vector = cv.fit_transform(docs)
    save_pickle(word_count_vector,"lab3/data/modified","word_count_vector.pkl",'wb')
    save_pickle(cv, "model", "count_vectorizer_v1.pkl", 'wb')
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    save_pickle(tfidf_transformer, "model", "tfidf_transformer_v1.pkl", 'wb')

def main():
    documents = preprocess_docs('isw_reports_txt')
    if not os.path.exists("preprocessed_reports"):
        os.mkdir("preprocessed_reports")
    for i in range(len(documents)):
        write_document(documents[i], "preprocessed_reports", f"report{i}.txt")
    documents_to_vec(documents)

