import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# pip install scikit-learn
# pip install pandas

# Sample user-item interaction data (0: no interaction, 1: interaction)
data = {
    'User1': [1, 1, 0, 0, 0],
    'User2': [0, 1, 1, 0, 0],
    'User3': [1, 0, 0, 0, 1],
    'User4': [0, 0, 1, 1, 0],
    'User5': [1, 1, 1, 0, 1],
}

user_item_df = pd.DataFrame(data, index=['Item1', 'Item2', 'Item3', 'Item4', 'Item5']).T

# Calculate user similarity using cosine similarity
user_similarity = cosine_similarity(user_item_df)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_df.index, columns=user_item_df.index)

def get_user_recommendations(user_id, user_item_df, user_similarity_df, n=2):
    user_vector = user_item_df.loc[user_id].values.reshape(1, -1)
    user_similarity_vector = user_similarity_df[user_id].values.reshape(1, -1)

    # Weighted average of item interactions based on user similarity
    recommendation_scores = np.dot(user_similarity_vector, user_item_df.values) / np.sum(np.abs(user_similarity_vector))

    # Exclude items the user has already interacted with
    recommendation_scores[:, user_vector.flatten() > 0] = 0

    # Get indices of top recommendations
    top_indices = np.argsort(recommendation_scores[0])[::-1][:n]

    # Get the names of the top recommended items
    top_recommendations = user_item_df.columns[top_indices]

    return top_recommendations

# Example usage:
user_id = 'User1'
recommended_items = get_user_recommendations(user_id, user_item_df, user_similarity_df)
print(f"Recommended items for {user_id}: {recommended_items}")