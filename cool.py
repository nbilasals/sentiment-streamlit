from matplotlib import font_manager
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import joblib
import csv
import os
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.exceptions import NotFittedError
import pickle
sns.set_theme(color_codes=True)

# Tambahin custom CSS buat desain aplikasi
st.markdown("""
    <style>
    /* Background utama hitam */
    body {
        background-color: white;
        color: white;
    }
    /* Header */
    .stApp header {
        background-color: #333;
        color: #4CAF50;
    }
    /* Subheader styling */
    .stSubheader {
        color: #4CAF50;
        text-align: center;
    }
    /* Dataframe styling */
    .stDataFrame {
        color: white;
        background-color: #333;
    }
    /* Table cell styling */
    .stDataFrame .st-ec {
        color: white;
    }
    /* Download button */
    .stDownloadButton {
        background-color: #4CAF50;
        color: white;
    }
    /* Adjusting text input */
    .stTextInput {
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Load the saved vectorizer
with open('data/tokenizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Load logistic regression model
model = joblib.load(os.path.join('data', 'model.joblib'))

# Load lexicon
lexicon_positive = {}
with open(os.path.join('data', 'lexicon_positive_ver1.csv'), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        lexicon_positive[row[0]] = int(row[1])

lexicon_negative = {}
with open(os.path.join('data', 'lexicon_negative_ver1.csv'), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        lexicon_negative[row[0]] = int(row[1])


def sentiment_analysis_lexicon_indonesia(text):
    score = 0
    for word in text:
        if word in lexicon_positive:
            score += lexicon_positive[word]
        if word in lexicon_negative:
            score -= lexicon_negative[word]
    if score > 0:
        polarity = 'positive'
    elif score < 0:
        polarity = 'negative'
    else:
        polarity = 'neutral'
    return score, polarity


font_path = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')[0]


# def create_charts(df):
#     # Logistic Regression Sentiment Analysis
#     st.subheader('Sentiment Analysis (Logistic Regression)')
#     fig, ax = plt.subplots()
#     sns.countplot(x='sentiment_lr', data=df, ax=ax)
#     st.pyplot(fig)

#     st.subheader('Sentiment Distribution (Logistic Regression)')
#     sentiment_counts_lr = df['sentiment_lr'].value_counts()
#     fig, ax = plt.subplots()
#     ax.pie(sentiment_counts_lr, labels=sentiment_counts_lr.index, autopct='%1.1f%%')
#     st.pyplot(fig)

#     st.subheader('Word Cloud (Logistic Regression)')
#     text_lr = ' '.join([' '.join(tokens) for tokens in df['processed_text']])
#     wordcloud_lr = WordCloud(width=800, height=400).generate(text_lr)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_lr, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)

#     st.subheader('Word Cloud for Positive Reviews (Logistic Regression)')
#     positive_text_lr = ' '.join([' '.join(
#         tokens) for tokens in df[df['sentiment_lr'] == 'positive']['processed_text']])
#     wordcloud_positive_lr = WordCloud(
#         width=800, height=400).generate(positive_text_lr)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_positive_lr, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)

#     st.subheader('Word Cloud for Neutral Reviews (Logistic Regression)')
#     neutral_text_lr = ' '.join([' '.join(
#         tokens) for tokens in df[df['sentiment_lr'] == 'neutral']['processed_text']])
#     wordcloud_neutral_lr = WordCloud(
#         width=800, height=400).generate(neutral_text_lr)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_neutral_lr, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)

#     st.subheader('Word Cloud for Negative Reviews (Logistic Regression)')
#     negative_text_lr = ' '.join([' '.join(
#         tokens) for tokens in df[df['sentiment_lr'] == 'negative']['processed_text']])
#     wordcloud_negative_lr = WordCloud(
#         width=800, height=400).generate(negative_text_lr)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_negative_lr, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)
#     positive_reviews_lr = df[df['sentiment_lr'] == 'positive']
#     positive_reviews_sorted_lr = positive_reviews_lr.sort_values(
#         by='polarity_score', ascending=False).head(10)
#     st.subheader('Top 10 Positive Reviews (Logistic Regression)')
#     st.dataframe(positive_reviews_sorted_lr[['Komentar', 'sentiment_lr']])

#     negative_reviews_lr = df[df['sentiment_lr'] == 'negative']
#     negative_reviews_sorted_lr = negative_reviews_lr.sort_values(
#         by='polarity_score', ascending=False).head(10)
#     st.subheader('Top 10 Negative Reviews (Logistic Regression)')
#     st.dataframe(negative_reviews_sorted_lr[['Komentar', 'sentiment_lr']])

#     neutral_reviews_lr = df[df['sentiment_lr'] == 'neutral']
#     neutral_reviews_sorted_lr = neutral_reviews_lr.sort_values(
#         by='polarity_score', ascending=False).head(10)
#     st.subheader('Top 10 Neutral Reviews (Logistic Regression)')
#     st.dataframe(neutral_reviews_sorted_lr[['Komentar', 'sentiment_lr']])

#     # Lexicon Based Sentiment Analysis
#     st.subheader('Sentiment Analysis (Lexicon Based)')
#     fig, ax = plt.subplots()
#     sns.countplot(x='sentiment_lexicon', data=df, ax=ax)
#     st.pyplot(fig)

#     st.subheader('Sentiment Distribution (Lexicon Based)')
#     sentiment_counts_lexicon = df['sentiment_lexicon'].value_counts()
#     fig, ax = plt.subplots()
#     ax.pie(sentiment_counts_lexicon,
#            labels=sentiment_counts_lexicon.index, autopct='%1.1f%%')
#     st.pyplot(fig)

#     st.subheader('Word Cloud (Lexicon-based)')
#     text_lexicon = ' '.join([' '.join(tokens)
#                             for tokens in df['processed_text']])
#     wordcloud_lexicon = WordCloud(width=800, height=400).generate(text_lexicon)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_lexicon, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)

#     st.subheader('Word Cloud for Positive Reviews (Lexicon-based)')
#     positive_text_lexicon = ' '.join([' '.join(
#         tokens) for tokens in df[df['sentiment_lexicon'] == 'positive']['processed_text']])
#     wordcloud_positive = WordCloud(
#         width=800, height=400).generate(positive_text_lexicon)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_positive, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)

#     st.subheader('Word Cloud for Neutral Reviews (Lexicon-based)')
#     neutral_text_lexicon = ' '.join([' '.join(
#         tokens) for tokens in df[df['sentiment_lexicon'] == 'neutral']['processed_text']])
#     wordcloud_neutral = WordCloud(
#         width=800, height=400).generate(neutral_text_lexicon)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_neutral, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)

#     st.subheader('Word Cloud for Negative Reviews (Lexicon-based)')
#     negative_text_lexicon = ' '.join([' '.join(
#         tokens) for tokens in df[df['sentiment_lexicon'] == 'negative']['processed_text']])
#     wordcloud_negative = WordCloud(
#         width=800, height=400).generate(negative_text_lexicon)
#     fig, ax = plt.subplots()
#     ax.imshow(wordcloud_negative, interpolation='bilinear')
#     ax.axis('off')
#     st.pyplot(fig)

#     positive_reviews_lexicon = df[df['sentiment_lexicon'] == 'positive']
#     positive_reviews_sorted_lexicon = positive_reviews_lexicon.sort_values(
#         by='polarity_score', ascending=False).head(10)
#     st.subheader('Top 10 Positive Reviews (Lexicon-based)')
#     st.dataframe(positive_reviews_sorted_lexicon[[
#                  'Komentar', 'sentiment_lexicon']])

#     negative_reviews_lexicon = df[df['sentiment_lexicon'] == 'negative']
#     negative_reviews_sorted_lexicon = negative_reviews_lexicon.sort_values(
#         by='polarity_score', ascending=False).head(10)
#     st.subheader('Top 10 Negative Reviews (Lexicon-based)')
#     st.dataframe(negative_reviews_sorted_lexicon[[
#                  'Komentar', 'sentiment_lexicon']])

#     neutral_reviews_lexicon = df[df['sentiment_lexicon'] == 'neutral']
#     neutral_reviews_sorted_lexicon = neutral_reviews_lexicon.sort_values(
#         by='polarity_score', ascending=False).head(10)
#     st.subheader('Top 10 Neutral Reviews (Lexicon Based)')
#     st.dataframe(neutral_reviews_sorted_lr[['Komentar', 'sentiment_lexicon']])

def styled_subheader(text):
    st.markdown(
        f"<h2 style='text-align: center; color: #4CAF50;'>{text}</h2>", unsafe_allow_html=True)


def create_charts(df):

    # Get sentiment counts
    sentiment_counts_lexicon = df['sentiment_lexicon'].value_counts()
    sentiment_counts_lr = df['sentiment_lr'].value_counts()

    # Show value counts in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Value Counts (Lexicon Based)")
        st.write(sentiment_counts_lexicon)
    with col2:
        st.markdown("### Value Counts (Logistic Regression)")
        st.write(sentiment_counts_lr)

    # Logistic Regression Sentiment Analysis
    styled_subheader('Sentiment Analysis (Logistic Regression)')
    fig, ax = plt.subplots()
    sns.countplot(x='sentiment_lr', data=df, ax=ax, palette='Set2')
    st.pyplot(fig)

    styled_subheader('Sentiment Distribution (Logistic Regression)')
    sentiment_counts_lr = df['sentiment_lr'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts_lr, labels=sentiment_counts_lr.index,
           autopct='%1.1f%%', colors=sns.color_palette('Set2'))
    st.pyplot(fig)

    styled_subheader('Word Clouds (Logistic Regression)')
    col1, col2, col3 = st.columns(3)

    with col1:
        positive_text_lr = ' '.join([' '.join(
            tokens) for tokens in df[df['sentiment_lr'] == 'positive']['processed_text']])
        if positive_text_lr:
            st.markdown(
                "<h3 style='text-align: center;'>Positive</h3>", unsafe_allow_html=True)
            wordcloud_positive_lr = WordCloud(
                width=400, height=400, colormap='Greens', background_color='white').generate(positive_text_lr)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_positive_lr, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

    with col2:
        neutral_text_lr = ' '.join([' '.join(
            tokens) for tokens in df[df['sentiment_lr'] == 'neutral']['processed_text']])
        if neutral_text_lr:
            st.markdown("<h3 style='text-align: center;'>Neutral</h3>",
                        unsafe_allow_html=True)
            wordcloud_neutral_lr = WordCloud(
                width=400, height=400, colormap='Blues', background_color='white').generate(neutral_text_lr)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_neutral_lr, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

    with col3:
        negative_text_lr = ' '.join([' '.join(
            tokens) for tokens in df[df['sentiment_lr'] == 'negative']['processed_text']])
        if negative_text_lr:
            st.markdown(
                "<h3 style='text-align: center;'>Negative</h3>", unsafe_allow_html=True)
            wordcloud_negative_lr = WordCloud(
                width=400, height=400, colormap='Reds', background_color='white').generate(negative_text_lr)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_negative_lr, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

    positive_reviews_lr = df[df['sentiment_lr'] == 'positive']
    positive_reviews_sorted_lr = positive_reviews_lr.sort_values(
        by='polarity_score', ascending=False).head(10)
    styled_subheader('Top 10 Positive Reviews (Logistic Regression)')
    st.dataframe(positive_reviews_sorted_lr[['Komentar', 'sentiment_lr']])

    negative_reviews_lr = df[df['sentiment_lr'] == 'negative']
    negative_reviews_sorted_lr = negative_reviews_lr.sort_values(
        by='polarity_score', ascending=False).head(10)
    styled_subheader('Top 10 Negative Reviews (Logistic Regression)')
    st.dataframe(negative_reviews_sorted_lr[['Komentar', 'sentiment_lr']])

    neutral_reviews_lr = df[df['sentiment_lr'] == 'neutral']
    neutral_reviews_sorted_lr = neutral_reviews_lr.sort_values(
        by='polarity_score', ascending=False).head(10)
    styled_subheader('Top 10 Neutral Reviews (Logistic Regression)')
    st.dataframe(neutral_reviews_sorted_lr[['Komentar', 'sentiment_lr']])

    # Lexicon Based Sentiment Analysis
    styled_subheader('Sentiment Analysis (Lexicon Based)')
    fig, ax = plt.subplots()
    sns.countplot(x='sentiment_lexicon', data=df, ax=ax, palette='Set3')
    st.pyplot(fig)

    styled_subheader('Sentiment Distribution (Lexicon Based)')
    sentiment_counts_lexicon = df['sentiment_lexicon'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts_lexicon, labels=sentiment_counts_lexicon.index,
           autopct='%1.1f%%', colors=sns.color_palette('Set3'))
    st.pyplot(fig)

    styled_subheader('Word Clouds (Lexicon-based)')
    col1, col2, col3 = st.columns(3)

    with col1:
        positive_text_lexicon = ' '.join([' '.join(
            tokens) for tokens in df[df['sentiment_lexicon'] == 'positive']['processed_text']])
        if positive_text_lexicon:
            st.markdown(
                "<h3 style='text-align: center;'>Positive</h3>", unsafe_allow_html=True)
            wordcloud_positive_lexicon = WordCloud(
                width=400, height=400, colormap='Greens', background_color='white').generate(positive_text_lexicon)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_positive_lexicon, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

    with col2:
        neutral_text_lexicon = ' '.join([' '.join(
            tokens) for tokens in df[df['sentiment_lexicon'] == 'neutral']['processed_text']])
        if neutral_text_lexicon:
            st.markdown("<h3 style='text-align: center;'>Neutral</h3>",
                        unsafe_allow_html=True)
            wordcloud_neutral_lexicon = WordCloud(
                width=400, height=400, colormap='Blues', background_color='white').generate(neutral_text_lexicon)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_neutral_lexicon, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

    with col3:
        negative_text_lexicon = ' '.join([' '.join(
            tokens) for tokens in df[df['sentiment_lexicon'] == 'negative']['processed_text']])
        if negative_text_lexicon:
            st.markdown(
                "<h3 style='text-align: center;'>Negative</h3>", unsafe_allow_html=True)
            wordcloud_negative_lexicon = WordCloud(
                width=400, height=400, colormap='Reds', background_color='white').generate(negative_text_lexicon)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_negative_lexicon, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

    positive_reviews_lexicon = df[df['sentiment_lexicon'] == 'positive']
    positive_reviews_sorted_lexicon = positive_reviews_lexicon.sort_values(
        by='polarity_score', ascending=False).head(10)
    styled_subheader('Top 10 Positive Reviews (Lexicon-based)')
    st.dataframe(positive_reviews_sorted_lexicon[[
                 'Komentar', 'sentiment_lexicon']])

    negative_reviews_lexicon = df[df['sentiment_lexicon'] == 'negative']
    negative_reviews_sorted_lexicon = negative_reviews_lexicon.sort_values(
        by='polarity_score', ascending=False).head(10)
    styled_subheader('Top 10 Negative Reviews (Lexicon-based)')
    st.dataframe(negative_reviews_sorted_lexicon[[
                 'Komentar', 'sentiment_lexicon']])

    neutral_reviews_lexicon = df[df['sentiment_lexicon'] == 'neutral']
    neutral_reviews_sorted_lexicon = neutral_reviews_lexicon.sort_values(
        by='polarity_score', ascending=False).head(10)
    styled_subheader('Top 10 Neutral Reviews (Lexicon Based)')
    st.dataframe(neutral_reviews_sorted_lexicon[[
                 'Komentar', 'sentiment_lexicon']])


def preprocess_text(text, indo_stopwords):
    # Convert text to lowercase
    text = text.lower()

    # Remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove Twitter usernames
    text = re.sub("@[A-Za-z0-9_]+", "", text)

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Remove superscript
    superscript_pattern = re.compile("["u"\U00002070"
                                     u"\U000000B9"
                                     u"\U000000B2-\U000000B3"
                                     u"\U00002074-\U00002079"
                                     u"\U0000207A-\U0000207E"
                                     u"\U0000200D"
                                     "]+", flags=re.UNICODE)
    text = superscript_pattern.sub(r'', text)

    # Remove hashtags
    text = re.sub("#[A-Za-z0-9_]+", "", text)

    # Remove word repetition
    text = re.sub(r'(.)\1+', r'\1\1', text)

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    # Remove small words
    text = re.sub(r'\b\w{1,3}\b', '', text)

    # Remove stopwords
    tokens = word_tokenize(text)
    filtered_tokens = [
        token for token in tokens if token.lower() not in indo_stopwords]
    text = ' '.join(filtered_tokens)

    # Stemming
    stem = StemmerFactory()
    create_stem = stem.create_stemmer()
    text = create_stem.stem(text)

    return text


# def vectorize_text(text_data):
#     # Initialize TfidfVectorizer
#     tfidf_vectorizer = TfidfVectorizer(use_idf=True, smooth_idf=False)
#     # Fit the vectorizer on the processed text data
#     tfidf_vectorizer.fit(df['processed_text'])
#     # transform the text data
#     tfidf_vectors = tfidf_vectorizer.transform(text_data)

#     return tfidf_vectors


def analyze_sentiment(df):
    # Preprocess text
    indo_stopwords = stopwords.words('indonesian')
    df['processed_text'] = df['Komentar'].apply(
        lambda x: preprocess_text(x, indo_stopwords))
    try:
        # Vectorize text using fitted TF-IDF vectorizer
        tfidf_vectors = vectorizer.transform(df['processed_text'])

        # Sentiment analysis using logistic regression model
        df['sentiment_lr'] = model.predict(tfidf_vectors)
    except NotFittedError:
        st.error(
            "The TF-IDF vectorizer is not fitted. Please fit the vectorizer before using it for prediction.")
    # Map numeric labels to string labels
    label_mapping = {0: 'neutral', 1: 'negative', 2: 'positive'}
    df['sentiment_lr'] = df['sentiment_lr'].map(label_mapping)

    # Sentiment analysis using lexicon-based method
    df['processed_text'] = df.processed_text.str.split()
    results = df['processed_text'].apply(sentiment_analysis_lexicon_indonesia)
    results = list(zip(*results))
    df['polarity_score'] = results[0]
    df['sentiment_lexicon'] = results[1]

    return df


st.title('Analisis Sentimen QRIS')

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Baca data dari file CSV
    df = pd.read_csv(uploaded_file)

    # Cek apakah kolom 'Komentar' ada dalam dataframe
    if 'Komentar' not in df.columns:
        st.error("File CSV harus memiliki kolom bernama 'Komentar'.")
    else:
        st.success(
            "File CSV berhasil diunggah. Kolom 'Komentar' ditemukan. Menganalisis sentimen.....")
        st.write(df.head())

        # Preprocess text and perform sentiment analysis
        df = analyze_sentiment(df)

        styled_subheader(
            'Hasil Analisis Sentimen dengan Logistic Regression vs Lexicon-Based')

        st.write(df)

        # Create charts
        create_charts(df)

        datas = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download data as CSV",
            data=datas,
            file_name="sentiment_analysis.csv",
            mime="text/csv"
        )
