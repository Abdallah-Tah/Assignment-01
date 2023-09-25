import pandas as pd
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

path = input("Enter the directory path: ")

files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.html')]

data_list = []

for file in tqdm(files, desc="Processing files"):
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        for math in soup.find_all('math'):
            math.extract()
        
        title_tag = soup.select_one('.ltx_title_document')
        title = title_tag.text.strip() if title_tag else "N/A"
        
        authors = []
        emails = []
        affiliations = []
        
        author_tags = soup.select('.ltx_creator.ltx_role_author')
        
        for author_tag in author_tags:
            author_name_tag = author_tag.select_one('.ltx_personname')
            email_tag = author_tag.select_one('.ltx_role_email a')
            affiliation_tag = author_tag.select_one('.ltx_role_address')
            
            authors.append(author_name_tag.text.strip() if author_name_tag else "N/A")
            emails.append(email_tag.text.strip() if email_tag else "N/A")
            affiliations.append(affiliation_tag.text.strip() if affiliation_tag else "N/A")
        
        abstract_tag = soup.select_one('.ltx_abstract .ltx_p')
        abstract = abstract_tag.text.strip() if abstract_tag else "N/A"
        
        keyword_tag = soup.select_one('.ltx_classification')
        keywords = [k.strip() for k in keyword_tag.text.replace("keywords:", "").split(",")] if keyword_tag else ["N/A"]
        
        data_list.append({
            "Title": title,
            "Authors": ", ".join(authors),
            "Emails": ", ".join(emails),
            "Affiliations": ", ".join(affiliations),
            "Abstract": abstract,
            "Keywords": ", ".join(keywords)
        })

if not os.path.exists('output'):
    os.makedirs('output')

data_frame = pd.DataFrame(data_list)
data_frame.to_csv('./output/assignment01.tsv', sep='\t', index=False)
