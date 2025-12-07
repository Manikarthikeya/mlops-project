import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Real-Time Recommendation System OPS", layout="wide")

st.title(" Real-Time Recommendation System Ops")
st.write("This is a simple real-time recommendation system using TF-IDF + Cosine Similarity.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["combined"] = df["category"] + " " + df["tags"]
    return df

df = load_data()

# Vectorize
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["combined"])

# Recommendation function
def recommend_items(user_query, top_k=3):
    query_vec = vectorizer.transform([user_query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = scores.argsort()[-top_k:][::-1]
    return df.iloc[top_indices]

# User Input
st.subheader(" Enter your interest or need (real-time input)")
user_input = st.text_input("Example: running shoes, office shirt, travel bag")

if st.button("Get Real-Time Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter something!")
    else:
        st.subheader(" Recommended Items:")
        recs = recommend_items(user_input)

        for _, row in recs.iterrows():
            st.markdown(f"""
            ### {row['item_name']}
            - **Category:** {row['category']}
            - **Tags:** {row['tags']}
            """)

