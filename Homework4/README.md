# Homework 4 README: Social Media Post Analysis

## Project Overview
This analysis explores a social media dataset containing user posts, likes, shares, hashtags, and timestamps. The goal was to clean and analyze this data for sentiment, engagement, and trending topics.

---

## Tasks Completed

1. **Data Cleaning**
    - Removed URLs, emojis, mentions (@), and extracted hashtags.
    - Handled missing values (likes, shares, post content).

2. **Data Analysis**
    - Calculated average engagement (likes + shares) for each user.
    - Identified top 3 users with the highest average engagement.
    - Extracted top 5 most frequent hashtags.

3. **Sentiment Analysis**
    - Classified posts as Positive, Neutral, or Negative using TextBlob.
    - Calculated sentiment distribution and average sentiment score per user.

4. **Visualization**
    - Word cloud of top hashtags.
    - Line plot of monthly post frequency.
    - Scatter plot of likes vs shares showing positive correlation.

---

## Key Insights

- Most users had **neutral or slightly positive sentiment**, indicating general satisfaction or neutral discussions.
- The top 3 hashtags were: `#sunnyday`, `#fun`, and `#travel`, showing user interests leaned toward lifestyle and leisure.
- There’s a **moderate positive correlation** between likes and shares, meaning popular posts tend to be shared more.
- Posting activity was higher in **[insert peak months]**, possibly indicating seasonal engagement spikes.

---

## Included Files

- `cleaned_data.csv`: Final processed dataset
- `wordcloud.png`: Most common hashtags
- `posts_per_month.png`: Time series post frequency
- `likes_vs_shares_scatter.png`: Engagement relationship
- `test_social_media.py`: Unit tests
- `main_analysis.py`: Main analysis script
- `README.txt`: This file

## Insights: Sentiment Classification Challenges

### Unit Test Observation
During unit testing, one notable failure occurred in the sentiment classification function. Specifically, the test case for the phrase **"It's okay"** was consistently misclassified.

### What Happened
- The test failed only for **"It's okay"**, which was expected to be **neutral** but was misclassified (either as positive or negative) by the sentiment analysis model.
- The sentiment score from **TextBlob** returned a polarity that didn't align well with the intuitive sentiment of the phrase.
- Adjusting the classification threshold values (e.g., using wider neutral zones like ±0.3) did **not** resolve the issue.

### Insight
This suggests a limitation of **rule-based sentiment analyzers like TextBlob**, which often struggle with subtle or context-dependent language (e.g., sarcasm, mild opinions like "it's okay"). A more nuanced model like **VADER** or **BERT-based models** would likely perform better for such borderline or neutral content in future implementations.
