import streamlit as st
from my_component import my_component

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.

sample_llm_response='This result comes from Excerpt 1. Excerpt 2 is not mentioned, but maybe you can find what you want in excerpt 3?'

excerpt_selected = my_component(llm_response=sample_llm_response)
st.markdown(f"You've selected {excerpt_selected}")

st.markdown("---")