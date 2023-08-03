import nltk
import random
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier

nltk.download('movie_reviews')
nltk.download('stopwords')

# Create a list of tuples where each tuple contains a review text and its corresponding sentiment (positive/negative)
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

# Shuffle the documents to ensure randomness
random.shuffle(documents)

# Define a set of stopwords to remove irrelevant words
stop_words = set(stopwords.words('english'))

# Define a function to extract features from the text data
def extract_features(document):
    words = set(document)
    useful_words = [word for word in words if word.lower() not in stop_words]
    features = {word: True for word in useful_words}
    return features

# Create feature sets for the positive and negative reviews
featuresets = [(extract_features(doc), sentiment) for (doc, sentiment) in documents]

# Define the split ratio (80% for training, 20% for testing)
split_ratio = 0.8
split_index = int(len(featuresets) * split_ratio)

# Split the dataset
train_set = featuresets[:split_index]
test_set = featuresets[split_index:]

classifier = NaiveBayesClassifier.train(train_set)

accuracy = nltk.classify.accuracy(classifier, test_set)
print(f"Accuracy: {accuracy * 100:.2f}%")

def predict_sentiment(text):
    words = word_tokenize(text)
    features = extract_features(words)
    sentiment = classifier.classify(features)
    return sentiment

# Example usage
text_to_analyze = "This is a really bad movie. I would not recommend watching it."
predicted_sentiment = predict_sentiment(text_to_analyze)
print(f"Predicted sentiment: {predicted_sentiment}")