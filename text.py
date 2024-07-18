import ast
response = """
```python
visa_form = {
    "Name": "Jali-Ligali Nafisat Temitope",
    "Date of Birth": "18th September 1989",
    "Marital Status": "Married",
    "Product Type": "EEP/PNP",
    "IELTS scores for Principal applicant": "Listening- 8.5, Reading- 8.0, Speaking- 7.5, and Writing- 7.5 projected IELTS",
    "IELTS scores for Dependent spouse": "Listening 8.0 -, Reading 7.0 -, Speaking 7.0 -, and Writing 7.0 Projected IELTS",
    "Available degrees for Principal applicant": "Masters degree",
    "Available degrees for Dependent spouse": "Bachelors",
    "Years of work experience for Principal applicant": "more than 3 years",
    "Have you had a previous Canada visa application? If yes, how many?": "None",
    "Details of Previous Canada visa application:(date/month/year , start and end date the academic qualification that was was filled, start and end dates off all work experience filled )": "None",
    "Do you have family members who reside in Canada as permanent residence? If yes, specify your relationship with them and the province in which they reside.": "None",
    "Do you currently reside in Nigeria? If No, specify the country you currently reside and the date ( Date/Month/Year) you left Nigeria:": "Yes"
}
```
"""
start_index = response.index("{")
end_index = response.index("}") 
#dict_str = response[start_index]
#visa_form = ast.literal_eval(dict_str)
def convert_to_dict(data_string):
    try:
# Use ast.literal_eval() for safe parsing
        return ast.literal_eval(data_string)
    except SyntaxError as e:
        raise ValueError(f"Invalid dictionary format: {data_string}") from e
#print(start_index,end_index)
#print(response[start_index+1:end_index])
data_string=response[start_index+1:end_index]

try:
    data_dict = convert_to_dict(data_string)
    print(data_dict)
except ValueError as e:
    print(e)