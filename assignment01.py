import pandas as pd
from bs4 import BeautifulSoup
import os

##########################################################################################
#  Assignment 01: Extracting data from HTML files using BeautifulSoup
#  COS 457 Database Systems - Fall 2023 - Professor Behrooz Mansouri 
#  By: Abadallah Mohamed
#  Date: 09/12/2023
#  Description: This program extracts data from HTML files using BeautifulSoup and saves
#               the extracted data to a TSV file.
##########################################################################################

# Set the path
path = "./papers/01/"

# List all HTML files in the directory
files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.html')]

# Initialize an empty list to store the extracted data
data_list = []

# Process each file
for file in files:
    print(f"Processing file: {os.path.basename(file)}")
    
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Remove all math tags to avoid math characters
        for math in soup.find_all('math'):
            math.extract()
        
        # Get title
        title_tag = soup.select_one('.ltx_title_document')
        title = title_tag.text if title_tag else "N/A"
        
        # Get authors, emails, affiliations
        authors = []
        emails = []
        affiliations = []
        
        author_tags = soup.select('.ltx_creator.ltx_role_author')
        
        for author_tag in author_tags:
            author_name_tag = author_tag.select_one('.ltx_personname')
            email_tag = author_tag.select_one('.ltx_role_email a')
            affiliation_tag = author_tag.select_one('.ltx_role_address')
            
            authors.append(author_name_tag.text if author_name_tag else "N/A")
            emails.append(email_tag.text if email_tag else "N/A")
            affiliations.append(affiliation_tag.text if affiliation_tag else "N/A")
        
        # Get abstract
        abstract_tag = soup.select_one('.ltx_abstract .ltx_p')
        abstract = abstract_tag.text if abstract_tag else "N/A"
        
        # Get keywords
        keyword_tag = soup.select_one('.ltx_classification')
        keywords = keyword_tag.text.replace("keywords:", "").split(",") if keyword_tag else ["N/A"]
        
        # Append data to the list
        data_list.append({
            "Title": title,
            "Authors": ", ".join(authors),
            "Emails": ", ".join(emails),
            "Affiliations": ", ".join(affiliations),
            "Abstract": abstract,
            "Keywords": ", ".join(keywords)
        })

# Save the extracted data to a CSV file
data_frame = pd.DataFrame(data_list)
#Check if the folder output exists if not create it
if not os.path.exists('output'):
    os.makedirs('output')
data_frame.to_csv('./output/assignment01.tsv', sep='\t', index=False)
print("Done!")

    
