import streamlit as st
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob

# Title and description
st.title("Product Sentiment Analysis")
st.write("Enter a keyword to search for tweets and analyze their sentiment.")

# User input
keyword = st.text_input("Enter a keyword to search for tweets")

# Fetch tweets and perform sentiment analysis
if keyword:
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} lang:en').get_items()):
        if i >= 100:
            break
        tweets.append(tweet.content)

    st.subheader(f"Analyzed Tweets ({len(tweets)} tweets):")
    for tweet in tweets:
        st.write(tweet)

    sentiment_scores = []
    positive_count = 0
    negative_count = 0
    for tweet in tweets:
        blob = TextBlob(tweet)
        sentiment_score = blob.sentiment.polarity
        sentiment_scores.append(sentiment_score)

        if sentiment_score > 0:
            positive_count += 1
        elif sentiment_score < 0:
            negative_count += 1

    # Average sentiment
    if sentiment_scores:
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        sentiment_label = "Positive" if average_sentiment > 0.09 else "Negative" if average_sentiment < 0.10 else "Neutral"
        st.subheader("Sentiment Analysis Results:")
        st.write("Average Polarity Score:", average_sentiment)
        st.write("Sentiment Label:", sentiment_label)
        st.write("Positive Tweets:", positive_count)
        st.write("Negative Tweets:", negative_count)