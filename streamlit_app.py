import streamlit as st
import requests
import time
import os

# --- Helper Functions ---

def initialize_session():
    """Initializes session variables."""
    if 'session_count' not in st.session_state:
        st.session_state.session_count = 0
    if 'block_time' not in st.session_state:
        st.session_state.block_time = None

def check_session_limit():
    """Checks if the user has reached the session limit and manages block time."""
    if st.session_state.block_time:
        time_left = st.session_state.block_time - time.time()
        if time_left > 0:
            st.error(f"You have reached your session limit. Please try again in {int(time_left)} seconds.")
            st.stop()

    if st.session_state.session_count >= 5:
        st.session_state.block_time = time.time() + 15 * 60  # Block for 15 minutes
        st.error("You have reached the session limit. Please wait for 15 minutes.")
        st.stop()

def call_generate_api(prompt):
    """Call the generate content API."""
    url = "https://r1api.onrender.com/generate"  # Replace with the actual API endpoint
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": prompt}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error generating content: {response.status_code} - {response.text}")
        return None

def call_regenerate_api(original_text):
    """Call the regenerate content API."""
    url = "https://r1api.onrender.com/regenerate"  # Replace with the actual API endpoint
    headers = {"Content-Type": "application/json"}
    payload = {"original_text": original_text}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error regenerating content: {response.status_code} - {response.text}")
        return None

# --- Streamlit App ---

# Initialize session tracking
initialize_session()

# App Title and Description
st.title("AI-Powered Content Generator")
st.write("Generate high-quality content using AI models and check its originality.")

# Prompt Input Field
prompt = st.text_area("Enter your prompt:", placeholder="Write a blog about AI trends in 2025.")

# Session management to check for block time and session limits
check_session_limit()

# Generate Content Button
if st.button("Generate Content"):
    if not prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        try:
            # Call the generate content API
            api_response = call_generate_api(prompt)

            if api_response:
                # Display the generated content
                st.subheader("Generated Content:")
                st.write(api_response.get("generated_text", "No content generated."))

                # Display search results
                st.subheader("Originality Check (Search Results):")
                search_results = api_response.get("search_results", [])
                if search_results:
                    for result in search_results[:5]:  # Show top 5 results
                        with st.expander(result['title']):
                            st.write(f"**Source:** [{result['link']}]({result['link']})")
                            st.write(f"**Snippet:** {result['snippet']}")
                            st.write("---")
                else:
                    st.write("No similar content found online. Your content is original.")

                # Increment session count
                st.session_state.session_count += 1

        except Exception as e:
            st.error(f"Error generating content: {e}")

# Regenerate Content Button
if st.button("Regenerate Content"):
    if 'generated_text' in st.session_state:
        original_text = st.session_state.generated_text
        regenerated_response = call_regenerate_api(original_text)

        if regenerated_response:
            st.subheader("Regenerated Content:")
            st.write(regenerated_response.get("regenerated_text", "No content generated."))
        else:
            st.error("Error regenerating content.")
    else:
        st.error("No generated content found to regenerate.")
