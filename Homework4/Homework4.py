import pandas as pd
import re

import textblob

df = pd.read_csv("social_media_posts.csv")

def clean_post(text):
    if pd.isnull(text):
        return "", []
    hashtags = re.findall(r"#(\w+)", text)
    text_no_emoji = re.sub(r"[^\w\s#@:/.\-]", "", text)
    text_no_url = re.sub(r"http[s]?://\S+", "", text_no_emoji)
    text_no_mentions = re.sub(r"@(\w+)", r"\1", text_no_url)
    cleaned = re.sub(r"#(\w+)", r"\1", text_no_mentions)

    return cleaned.strip(), hashtags

df[['cleaned_post_content', 'hashtags']] = df['post_content'].apply(lambda x: pd.Series(clean_post(x)))

print("Original Data type: ", df['post_date'].dtypes)
df['post_date'] = pd.to_datetime(df['post_date'])
print("New Data type: ", df['post_date'].dtypes)
print('\n')

df['likes'].fillna(df['likes'].median(), inplace=True)
df['shares'].fillna(df['shares'].mean(), inplace=True)
df['post_content'].fillna('no text', inplace=True)

avg_engagement = df.groupby('user_id')[['likes', 'shares']].mean()
avg_engagement['engagement'] = avg_engagement['likes'] + avg_engagement['shares']

top_users = avg_engagement.sort_values('engagement', ascending=False).head(3)

print("Top 3 users by average engagement:")
print(top_users)

from collections import Counter


all_hashtags = df['hashtags'].explode()
hashtag_counts = Counter(all_hashtags)


top_5_hashtags = hashtag_counts.most_common(5)

print("\nTop 5 most popular topics (hashtags):")
for tag, count in top_5_hashtags:
    print(f"{tag}: {count} times")

#!pip install textblob

from textblob import TextBlob

def get_sentiment(text):
    if not text or pd.isnull(text):
        return 0.0
    return TextBlob(text).sentiment.polarity

df['sentiment_score'] = df['cleaned_post_content'].apply(get_sentiment)

def classify_sentiment(score):
    if score > 0.1:
        return 'positive'
    elif score < -0.1:
        return 'negative'
    else:
        return 'neutral'

df['sentiment'] = df['sentiment_score'].apply(classify_sentiment)

sentiment_counts = df['sentiment'].value_counts()

print("Sentiment Distribution:")
print(sentiment_counts)

user_sentiment_avg = df.groupby('user_id')['sentiment_score'].mean().sort_values(ascending=False)

print("\nAverage Sentiment Score per User:")
print(user_sentiment_avg)


from wordcloud import WordCloud
import matplotlib.pyplot as plt

all_hashtags = df['hashtags'].explode().dropna().tolist()

hashtags_text = ' '.join(all_hashtags)

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(hashtags_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Hashtags")
plt.tight_layout()
plt.savefig("hashtag_wordcloud.png")
plt.show()

df['post_date'] = pd.to_datetime(df['post_date'])

df['year_month'] = df['post_date'].dt.to_period('M')

monthly_counts = df['year_month'].value_counts().sort_index()

monthly_counts.plot(kind='line', figsize=(10, 5), marker='o')
plt.title("Number of Posts per Month")
plt.xlabel("Month")
plt.ylabel("Number of Posts")
plt.grid(True)
plt.tight_layout()
plt.savefig("posts_per_month.png")
plt.show()


plt.figure(figsize=(8, 5))
plt.scatter(df['likes'], df['shares'], alpha=0.6, edgecolor='k')
plt.title("Correlation Between Likes and Shares")
plt.xlabel("Likes")
plt.ylabel("Shares")
plt.grid(True)
plt.tight_layout()
plt.savefig("likes_vs_shares_scatter.png")
plt.show()

correlation = df['likes'].corr(df['shares'])
print(f"Correlation coefficient: {correlation:.2f}")
