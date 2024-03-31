import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() # it will load all the enviroment variables.

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_promt,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_promt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    response = requests.get(uploaded_file)
    if response.status_code == 200:
        
        file_type = response.headers.get('content-type') # used for getting the type of source
        # byte_data = uploaded_file.getvalue() # use for getting the byte value out of image file.
        image_part = [
            {
                "mime_type": file_type, # file type required
                "data": response.content
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")
    

# initilizing streamlit application.
st.set_page_config(page_title="Gemini Health App")
st.header('Gemini Health App')
image_url = st.text_input("Paste the Link of image here:")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
if image_url:
#     # image = Image.open(str(image_url)
    st.image(image_url, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the total calories") 

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format
                dish name as header
               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

            also tell about that is it healthy or not?
"""

if submit:
    image_data = input_image_setup(image_url)
    response = get_gemini_response(input_prompt,image_data)
    st.header(response)
