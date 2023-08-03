#pip install nltk tensorflow
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import random
import json

nltk.download("punkt")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())

words = []
classes = []
documents = []
ignore_chars = ["?", "!", ".", ","]

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)

training_data = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    pattern_words, intent_tag = document
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(intent_tag)] = 1

    training_data.append([bag, output_row])

random.shuffle(training_data)
train_x = np.array([data[0] for data in training_data])
train_y = np.array([data[1] for data in training_data])

print("Training data created")


model = keras.Sequential(
    [
        layers.Dense(128, input_shape=(len(train_x[0]),), activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(len(train_y[0]), activation="softmax"),
    ]
)

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

print("LSTM model trained")

def chat_with_bot(user_input):
    results = model.predict(np.array([bag_of_words(user_input, words)]))[0]
    results_index = np.argmax(results)
    tag = classes[results_index]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            response = random.choice(intent["responses"])
            return response

    return "I'm not sure how to respond to that."

def bag_of_words(user_input, words):
    bag = [0] * len(words)
    user_words = nltk.word_tokenize(user_input)
    user_words = [lemmatizer.lemmatize(word.lower()) for word in user_words]

    for user_word in user_words:
        for i, word in enumerate(words):
            if word == user_word:
                bag[i] = 1

    return bag

print("Chatbot: Hi! I'm your chatbot. Type 'quit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Chatbot: Goodbye! Have a great day.")
        break
    response = chat_with_bot(user_input)
    print("Chatbot:", response)
