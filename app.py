from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("gemeni_api_key"))

# function to load gemenai 
model=genai.GenerativeModel('gemini-2.0-flash')

def get_gemini_response(input,image,prompt):
     response=model.generate_content([input,image[0],prompt])
     return response.text


def input_image_setup(uploaded_file):
     if uploaded_file is not None:
          
        #   Read the file type into the bytes
        bytes_data =uploaded_file.getvalue()
        
        image_parts=[
             {
                  "mime_type":uploaded_file.type,
                  "data":bytes_data
             }
        ]
        return image_parts
     else:
          raise FileNotFoundError("No file uploaded")
     

## initizaliation our streamlit app

st.set_page_config(page_title="Multiplanguage Invoice Extractor")

st.title("Multiplanguage Invoice Extractor")
input=st.text_input("Input prompt:- ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
     image=Image.open(uploaded_file)
     st.image(image,caption="uploaded Image", use_container_width=True)

submit=st.button("tell me about the invoice ")


input_prompt="""
Yoe are an expert in understanding invoices .We will uppload a image as in voice and you will have to answer any questions based on the uploaded invoives images 
"""



# After button is clicked 
if submit:
        try:
            image_data=input_image_setup(uploaded_file)
            response=get_gemini_response(input_prompt,image_data,input)
            st.subheader("Respose is ")
            st.write(response)
        except Exception as e:
            st.write(e)