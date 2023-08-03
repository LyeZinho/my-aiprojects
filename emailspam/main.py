"""
    csv data format:

    v       label   text                                                    label_num
    1990    span    "Hi, I'm calling about your car's extended warranty."   0
    1991    spam    "Hi, I'm calling about your car's extended warranty."   1
    1000    ham     "Hi, I'm calling about your car's extended warranty."   2

"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Load the dataset
data = pd.read_csv('spam_ham_dataset.csv')  # Replace 'spam_dataset.csv' with your dataset file

# Step 2: Data Preprocessing (cleaning not shown for simplicity)
X = data['text']  # Email text
y = data['label']  # 'spam' or 'ham' (target)

# Step 3: Feature Extraction
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Step 4: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Build and Train the Model
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Step 6: Evaluate the Model
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", report)

# Step 7: Use the Model to Predict (optional)
new_email = ["This is a spam email with fake offers!"]
new_email_vectorized = vectorizer.transform(new_email)
prediction = classifier.predict(new_email_vectorized)
print("Predicted label for the new email:", prediction[0])