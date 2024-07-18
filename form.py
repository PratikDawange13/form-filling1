from pypdf import PdfReader, PdfWriter
from pprint import pprint

"""
reader = PdfReader("new_form.pdf")
writer = PdfWriter()

page = reader.pages[0]
fields = reader.get_fields()
pprint(fields)

writer.append(reader)

writer.update_page_form_field_values(
     writer.pages[0],
     {"APPLICANT NAME": "Anjaney"},
     auto_regenerate=True,
 )

with open("filled-out.pdf", "wb") as output_stream:
     writer.write(output_stream)
     """

from pypdf import PdfReader, PdfWriter
from pprint import pprint

# Assume you have a dictionary with the data to fill in
form_data = {
    "APPLICANT NAME": "Anjaney",
    "GWF NUMBER": "ABCD1234",
    "PASSPORT NUMBER": "XYZ",
    # Add more fields and values as needed
}

reader = PdfReader("imm1294e_Onwuanma Linda.pdf")
writer = PdfWriter()

page = reader.pages[0]
fields = reader.get_fields()
pprint(fields)  # This will show you all available fields in the form

writer.append(reader)

# Update all fields for which we have data
writer.update_page_form_field_values(
    writer.pages[0],
    form_data,
    auto_regenerate=True,
)

with open("filled-out.pdf", "wb") as output_stream:
    writer.write(output_stream)