import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

df = pd.read_csv(r"./alltext.csv", encoding='ISO-8859-1')
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def predict_universities(new_review):
    model = Doc2Vec.load("my_model.doc2vec")
    uni_vectors = {df.iloc[i]['University']: model.docvecs[str(i)] for i in range(len(df))}
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    words = word_tokenize(new_review.lower())
    new_review_words = [w for w in words if not w in stop_words]
    new_review_vector = model.infer_vector(new_review_words)

    uni_similarity = {}
    for uni in uni_vectors.keys():  
        vec = uni_vectors[uni]
        sim = cosine_similarity(new_review_vector.reshape(1, -1), vec.reshape(1, -1))[0][0]
        uni_similarity[uni] = sim

    total_similarity = sum(uni_similarity.values())
    uni_probabilities = {uni: sim / total_similarity for uni, sim in uni_similarity.items()}

    top_unis = sorted(uni_probabilities, key=uni_probabilities.get, reverse=True)

    return uni_probabilities
