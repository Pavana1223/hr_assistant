import streamlit as st
from agent import answer_query

st.set_page_config(page_title="HR Assistant Agent", page_icon="🤖")

st.title("🤖 HR Assistant Agent Demo")
st.write("Ask any HR-related question about leaves, benefits, or company policies.")

# Input box for user question
query = st.text_input("Enter your question:")

if st.button("Ask"):
    if query.strip():
        response = answer_query(query)
        st.success(response)
    else:
        st.warning("Please type a question.")