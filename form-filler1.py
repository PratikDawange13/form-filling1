import streamlit as st
from pypdf import PdfReader, PdfWriter
from function import text_extractor_for_pdf
import os
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF
from pprint import pprint
from markdown_pdf import MarkdownPdf, Section

load_dotenv()

api_key = os.getenv("gemini_api_key")    
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title('Visa Form Filling')

st.header('Upload Questionnaire and Form')
uploaded_questionnaire = st.file_uploader("Upload Questionnaire PDF", type="pdf")
uploaded_form = st.file_uploader("Upload Form PDF", type="pdf")

if uploaded_questionnaire is not None and uploaded_form is not None:
    if st.button('Generate Filled Form'):
        client_info = text_extractor_for_pdf(uploaded_questionnaire.read())
        form_fields = text_extractor_for_pdf(uploaded_form.read())

        prompt1 = f"Please go through all the information provided below for a client who is applying for a visa"
        prompt2 = """Use the client information to fill the following visa form, output the result in form of 
          a dictionary where each field name is the key from visa form (Make sure the field spelling and case remains
          the exact same as there is in the visa form) and the information to be filled is the value. If information is not present for a 
          given field you can leave the value as an empty string."""
        response = model.generate_content([prompt1, client_info, prompt2, form_fields])

        # Step 5: Extract the dictionary from the response
        res = response.text

        st.subheader('Filled Form Details')
        #st.text(res)

        response = res[res.index("{") + 1:res.index("}")]
        lst = response.split('"')
        field_dict = dict(zip(lst[1::4], lst[3::4]))

        # Save initial filled form with PyPDF
        reader = PdfReader(uploaded_form)
        writer = PdfWriter()
        writer.append(reader)
        writer.update_page_form_field_values(
            writer.pages[0],
            field_dict,
            auto_regenerate=True,
        )

        intermediate_path = "intermediate_filled.pdf"
        with open(intermediate_path, "wb") as output_stream:
            writer.write(output_stream)

        # Modify fields with PyMuPDF and save to final output
        doc = fitz.open(intermediate_path)
        for page in doc:
            for field, value in field_dict.items():
                if value:  # Only insert non-empty values
                    rect = page.search_for(field)
                    if rect:
                        page.insert_text(rect[0].tl,  # Position on the page (top-left corner of the field)
                                         value,
                                         fontname="courier",  # Using 'courier' font
                                         fontsize=12,
                                         color=(0, 0, 0))  # RGB color: black

        final_output_path = "filled-out.pdf"
        doc.save(final_output_path)

        # Step 8: Send the pdf to streamlit
        with open(final_output_path, "rb") as pdf_file:
            st.download_button(
                label="Download Filled Form Details as PDF",
                data=pdf_file,
                file_name="filled_form_details.pdf",
                mime="application/pdf"
            )
