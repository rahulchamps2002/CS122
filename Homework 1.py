input_text= "Artificial intelligence (AI) is a branch of computer science that focuses on creating machines capable of performing tasks that would normally require human intelligence. These tasks include problem-solving, learning, decision-making, speech recognition, and visual perception. AI systems are designed to simulate human cognitive functions and can learn from experience, improving their performance over time. One of the main goals of AI is to create intelligent agents that can perform tasks autonomously without constant human intervention. AI technologies have been successfully implemented in various fields, such as robotics, healthcare, finance, and transportation. For example, AI-powered medical diagnostic systems can analyze medical images to detect diseases like cancer, while self-driving cars are capable of navigating streets and traffic without human input."


# your code goes here
# 1) Split the given text into individual sentences.

split_text = [sentence.strip() for sentence in input_text.strip().split('.') if sentence]
print(split_text)

# 2) For each sentence, split it into words, removing any punctuation marks and converting everything to lowercase.
punctuation = '(),.-'
split_words = []
for word in split_text:
    cleaned_sentence = "".join([char.lower() if char not in punctuation else " " for char in word])
    words = cleaned_sentence.split()
    split_words.append(words)
word_categories = [word for sentence in split_words for word in sentence]
# 3) Categorize Words by Length: Classify each word based on its length:
#   Words with length 3 or less: "Short"
#   Words with length between 4 and 6 (inclusive): "Medium"
#   Words with length greater than 6: "Long"

word_categories = [(word, "Short") if len(word) <= 3
                   else (word, "Medium") if 4 <= len(word) <= 6
else (word, "Long")
                   for word in word_categories]
print(word_categories)
# 4) For each sentence, store the words categorized by their length in a tuple (e.g., ("Short", ["cat", "dog"])).
wordDict = {}
for word,cat in word_categories:
    wordDict[cat].append(word)


tupleCategories = [(cat, words) for cat, words in wordDict.items()]
print(tupleCategories)
