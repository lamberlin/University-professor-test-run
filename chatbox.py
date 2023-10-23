import pandas as pd

dftext = pd.read_csv(r"./alltext.csv", encoding='ISO-8859-1')
from collections import defaultdict, Counter
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('vader_lexicon')
nltk.download('stopwords')
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))


def handle():
    # Extract keywords
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=stop_words, max_features=100)
    X = vectorizer.fit_transform(dftext['reviews_lemmatized'])
    features = vectorizer.get_feature_names()

    uni_keywords = defaultdict(list)
    keyword_sentiments = {}

    # Verify keyword, no longer grouping by sub_topic
    for i in range(len(dftext)):
        review = dftext.iloc[i]
        university = review['University']
        review_text = review['reviews']
        review_sentiment = review['sentiment']
        review_keywords = [features[index] for index in X[i].indices]

        # Use VADER to check emotions
        vader_result = sia.polarity_scores(review_text)
        vader_sentiment = 'positive' if vader_result['compound'] >= 0.05 else 'negative' if vader_result[
                                                                                                'compound'] <= -0.05 else 'neutral'

        for word in review_keywords:
            if word not in keyword_sentiments:
                word_sentiment = 'positive' if sia.polarity_scores(word)['compound'] >= 0.05 else 'negative' if \
                sia.polarity_scores(word)['compound'] <= -0.05 else 'neutral'
                keyword_sentiments[word] = word_sentiment

            if keyword_sentiments[word] == review_sentiment and vader_sentiment == review_sentiment:
                uni_keywords[university].append(word)

    uni_keyword_counts = {uni: Counter(keywords) for uni, keywords in uni_keywords.items()}
    return keyword_sentiments, uni_keyword_counts


def extract_keywords(text):
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=100)
    X = vectorizer.fit_transform([text])
    features = vectorizer.get_feature_names()
    return features


def predict_universities(new_review, new_review_sub_topic):
    keyword_sentiments, uni_keyword_counts = handle()
    # Assuming the comment is what they hope for in their future university
    new_review_keywords = extract_keywords(new_review)
    new_keywords = [word for word in new_review_keywords if
                    word in keyword_sentiments and keyword_sentiments[word] == 'positive']

    uni_scores = defaultdict(int)
    for uni, keyword_counts in uni_keyword_counts.items():
        for keyword in new_keywords:
            uni_scores[uni] += keyword_counts[keyword]

    total_count = sum(uni_scores.values())
    if total_count == 0:
        print("No matching universities found.")
        return
    uni_probabilities = {uni: (count / total_count) for uni, count in uni_scores.items()}

    top_unis = sorted(uni_probabilities, key=uni_probabilities.get, reverse=True)
    # for uni in top_unis:
    #     print(f"{uni}: {uni_probabilities[uni]:.2%}")
    return uni_probabilities

