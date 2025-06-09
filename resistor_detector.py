# resisort
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
from openai import OpenAI

# OpenAI setup
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.title("Resisort")
st.write("We've got you sorted.")

# Use Streamlit's built-in camera input
img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # Read image from buffer
    image = Image.open(img_file_buffer)

    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Show the image
    st.image(image, caption="Captured Resistor", use_container_width=True)

    # Convert to base64
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    if st.button("Analyze Resistor"):
        with st.spinner("Processing..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Identify this resistor"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                            ]
                        }
                    ],
                    max_tokens=100
                )
                result = response.choices[0].message.content
                st.success("Resistor Value:")
                st.write(result)

            except Exception as e:
                st.error(f"OpenAI API failed: {e}")
