import streamlit as st
import requests
import os

# Set up the API URL and API Key (you can replace this with your Flask API URL)
API_URL = 'http://localhost:5000/generate'  # Update this to your Flask API's URL
API_KEY = os.getenv('API_KEY')  # Set your environment variable or hardcode the key

# Function to call the Flask API
def call_flask_api(prompt):
    headers = {
        'Authorization': API_KEY  # API Key for authentication
    }
    
    # Prepare the payload
    data = {
        'prompt': prompt
    }
    
    try:
        # Send the POST request to the Flask API
        response = requests.post(API_URL, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"Failed to connect to the API: {str(e)}"}

# Streamlit App UI
def main():
    st.title("AI Content Generation")

    st.write("Enter a prompt, and the model will generate content for you.")
    
    # Text input for the user to provide a prompt
    prompt = st.text_area("Enter your prompt here:", "")
    
    if st.button("Generate"):
        if prompt:
            # Call Flask API to generate content
            response = call_flask_api(prompt)
            
            if 'error' in response:
                st.error(response['error'])
            else:
                st.subheader("Generated Content:")
                st.write(response['generated_text'])
                
                st.subheader("Search Results:")
                for result in response['search_results']:
                    st.write(f"- {result['title']}: {result['link']}")
        else:
            st.warning("Please enter a prompt before generating.")

if __name__ == '__main__':
    main()
