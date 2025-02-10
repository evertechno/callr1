import streamlit as st
import requests
import time
import random

# ---- Helper Functions ----

def initialize_session():
    """Initializes session state variables."""
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
            st.write("Upgrade to Pro for unlimited content generation.")
            st.stop()
        else:
            st.session_state.block_time = None

    if st.session_state.session_count >= 5:
        st.session_state.block_time = time.time() + 15 * 60  # Block for 15 minutes
        st.error("You have reached the session limit. Please wait for 15 minutes or upgrade to Pro.")
        st.write("Upgrade to Pro for unlimited content generation.")
        st.stop()

def call_api_for_content(prompt):
    """Call the hosted API for content generation."""
    api_url = "https://r1api.onrender.com/generate-content"  # API endpoint for content generation
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()  # Expecting the response to be in JSON format
        else:
            st.error(f"Error generating content: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"API request error: {e}")
        return None

def call_api_for_search(query):
    """Call the hosted API for searching similar content."""
    api_url = "https://r1api.onrender.com/search-web"  # API endpoint for web search
    headers = {"Content-Type": "application/json"}
    data = {"query": query}
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()  # Expecting the response to be a list of search results
        else:
            st.error(f"Error during web search: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"API request error: {e}")
        return []

# ---- Streamlit App ----

# App Title and Description
st.title("AI-Powered Ghostwriter")
st.write("Generate high-quality content and check for originality using the power of Generative AI and Google Search.")

# Initialize session tracking
initialize_session()

# Prompt Input Field
prompt = st.text_area("Enter your prompt:", placeholder="Write a blog about AI trends in 2025.")

# Session management to check for block time and session limits
check_session_limit()

# Generate Content Button
if st.button("Generate Response"):
    if not prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        try:
            # Call the external API for content generation
            result = call_api_for_content(prompt)
            if result:
                generated_text = result.get("generated_text", "")

                # Increment session count
                st.session_state.session_count += 1

                # Display the generated content
                st.subheader("Generated Content:")
                st.write(generated_text)

                # Call the external API for checking similar content
                search_results = call_api_for_search(generated_text)

                if search_results:
                    st.warning("Similar content found on the web:")
                    for result in search_results[:5]:  # Show top 5 results
                        with st.expander(result['title']):
                            st.write(f"**Source:** [{result['link']}]({result['link']})")
                            st.write(f"**Snippet:** {result['snippet']}")
                            st.write("---")

                    st.warning("To ensure 100% originality, you can regenerate the content.")
                    if st.button("Regenerate Content"):
                        regenerate_and_display_content(generated_text)
                else:
                    st.success("No similar content found online. Your content seems original!")

        except Exception as e:
            st.error(f"Error generating content: {e}")

# Regenerate Content and Ensure Originality
def regenerate_and_display_content(original_text):
    """Regenerates content and displays it after ensuring originality."""
    result = call_api_for_content(f"Rewrite the following content to make it original and distinct:\n\n{original_text}")
    if result:
        regenerated_text = result.get("generated_text", "")
        st.success("Content has been regenerated for originality.")
        st.subheader("Regenerated Content:")
        st.write(regenerated_text)

# Display regenerated content if available
if 'generated_text' in st.session_state:
    st.subheader("Regenerated Content (After Adjustments for Originality):")
    st.write(st.session_state.generated_text)
