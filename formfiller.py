import streamlit as st
from pypdf import PdfReader, PdfWriter
from function import text_extractor_for_pdf
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
from pprint import pprint
from markdown_pdf import MarkdownPdf, Section
 

#client_info= text_extractor_for_pdf("A.I Questionnaire and Response for JaliLigali Nafisat Temitope (2).pdf")
#client_info= text_extractor_for_pdf("Canada  Questionnaire.pdf")

# Step 3 extract text from the form pdf

#form_fields= text_extractor_for_pdf("C:/Users/DELL/Desktop/form-filling/final_form4.pdf")
#print(form_fields)

# Step 4 Feed both in the model 

api_key = os.getenv("gemini_api_key")    
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit app
st.title('Visa Form Filling')

st.header('Upload Questionnaire and Form')
uploaded_questionnaire = st.file_uploader("Upload Questionnaire PDF", type="pdf")
uploaded_form = st.file_uploader("Upload Form PDF", type="pdf")
if uploaded_questionnaire is not None and uploaded_form is not None:
    if st.button('Generate Filled Form'):
        client_info= text_extractor_for_pdf(uploaded_questionnaire.read())
        form_fields = text_extractor_for_pdf(uploaded_form.read())

        prompt1 = f"Please go through all the information provided below for a client who is applying for a visa" 
        prompt2 = """Use the client information to fill the following visa form, output the result in form of 
          a dictionary where each field name is the key from visa form (Make sure the field spelling and case remains
          the exact same as there is in the visa form) and the information to be filled is the value. If information is not present for a 
          given field you can leave the value as an empty string."""
        response= model.generate_content([prompt1,client_info,prompt2,form_fields ])


#Step 5 Extract the dictionary from the response
        res = response.text

        st.subheader('Filled Form Details')
        st.text(res)
#print(res)

#field_dict= dict(res[start_index+1:end_index])
        response = res[res.index("{")+1:res.index("}")]
        lst =response.split('"')
        field_dict = dict(zip(lst[1::4], lst[3::4]))
#print(field_dict)
#Step 6 Write the pdf

        reader = PdfReader(uploaded_form)
        #reader =PdfReader("imm1294e_Onwuanma Linda.pdf")
        writer = PdfWriter()

        page = reader.pages[0]
        fields = reader.get_fields()
        #pprint(fields)  # This will show you all available fields in the form

        writer.append(reader)
# Update all fields for which we have data
        writer.update_page_form_field_values(
        writer.pages[0],
        field_dict,
        auto_regenerate=True,
        )

        with open("filled-out.pdf", "wb") as output_stream:
            writer.write(output_stream)

#Step 8 Send the pdf to streamlit
        with open('filled-out.pdf', "rb") as pdf_file:
           # with open(output_pdf_path, "rb") as pdf_file:

            st.download_button(
                label="Download Filled Form Details as PDF",
                data=pdf_file,
                file_name="filled_form_details.pdf",
                mime="application/pdf"
            )
