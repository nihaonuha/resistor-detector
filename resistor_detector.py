import streamlit as st
import openai
import base64
from PIL import Image
import io

# Set your API key here
openai.api_key = st.secrets["openai"]["api-key"]

# Streamlit UI
st.set_page_config(page_title="Resistor Value Detector", layout="centered")
st.title("📷 Resistor Value Detector")
st.write("Upload a picture of a resistor, and AI will tell you its value.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show the image
    buffered = io.BytesIO()

    # convert to RGB if not already
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    if st.button("🔍 Analyze Resistor"):
        with st.spinner("Analyzing..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": "Identify the resistor value shown in this image based on the color bands."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                        ]}
                    ],
                    max_tokens=100
                )
                result = response['choices'][0]['message']['content']
                st.success("Resistor Value Detected:")
                st.write(result)

            except Exception as e:
                st.error(f"Error: {e}")
