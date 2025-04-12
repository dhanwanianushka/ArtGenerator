import streamlit as st
import openai
import os
import requests
from io import BytesIO
from PIL import Image
import base64

def main():
    # Set page title and layout
    st.set_page_config(page_title="Mandala Art Generator", layout="centered")
    
    # Title and description
    st.title("✨ Mandala Art Generator ✨")
    st.markdown("Enter a word as inspiration to generate a unique black and white mandala art piece.")
    
    # API key input
    api_key = st.text_input("Enter your OpenAI API key:", type="password", help="Your key is only stored for this session")
    
    # Save API key to session state
    if api_key:
        st.session_state.api_key = api_key
        openai.api_key = api_key
    
    # Check if API key is available
    if 'api_key' not in st.session_state:
        st.warning("Please enter your OpenAI API key to continue.")
        st.info("You can get an API key from [OpenAI](https://platform.openai.com/api-keys)")
        return
    
    # Word input
    word = st.text_input("Enter a word for inspiration:", placeholder="e.g. tranquility, ocean, harmony...")
    
    # Generate button
    if st.button("Generate Mandala", disabled=not word):
        with st.spinner("Creating your mandala art..."):
            try:
                # Create prompt for DALL-E
                prompt = f"Create a detailed black and white mandala art inspired by the concept of '{word}'. The mandala should be intricate, symmetrical, and feature geometric patterns. Monochromatic design with high contrast."
                
                # Generate image with DALL-E 3
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                    style="vivid"
                )
                
                # Get image URL
                image_url = response.data[0].url
                
                # Download the image
                image_response = requests.get(image_url)
                image = Image.open(BytesIO(image_response.content))
                
                # Convert PIL Image to bytes for downloading
                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # Display the image
                st.image(image, caption=f"Mandala inspired by '{word}'", use_column_width=True)
                
                # Download button
                st.download_button(
                    label="Download Mandala",
                    data=byte_im,
                    file_name=f"{word}_mandala.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Error generating image: {str(e)}")
                st.info("Please check your API key or try again later.")
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and OpenAI DALL-E 3")

if __name__ == "__main__":
    main()