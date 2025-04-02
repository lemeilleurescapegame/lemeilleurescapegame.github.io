import os
import requests
from bs4 import BeautifulSoup
import re
import yaml
from urllib.parse import urlparse

def format_multiline_text(text):
        return "\n    " + "\n    ".join(text.split("\n")) if text else ""
def clean_enseigne_name(name):
    # Remove line breaks, extra spaces, and replace hyphens if needed
    name = name.replace("\n", " ").strip()  # Remove newlines and trim
    name = re.sub(r'\s+', ' ', name)  # Replace multiple spaces with a single space
    return name

def get_base_url(url):
    # Parse the URL and return just the domain
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def extract_data_and_create_md():
    url = input("Enter the URL: ")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract last part of URL
    url_suffix = url.rstrip('/').split('/')[-1]
    
    # Extract title
    title_tag1 = soup.find('h1', class_='title')
    title = title_tag1.get_text(strip=True) if title_tag1 else ""
    
    # Extract theme, duree, and nb-joueur
    theme = duree = nb_joueur = ""
    
    # Extract theme from the given structure
    theme_label = soup.find('div', class_='addition-label', string="Thème")
    if theme_label:
        theme_body = theme_label.find_next_sibling('div', class_='addition-body')
        if theme_body:
            theme = theme_body.get_text(strip=True)
    duree_label = soup.find('p', class_='heading', string="Durée")
    if duree_label:
        duree_body = duree_label.find_next_sibling('div', class_='details')
        if duree_body:
            duree_span = duree_body.find('span', class_='is-hidden-mobile')
            if duree_span:
                duree = duree_span.get_text(strip=True)
    nb_joueur_label = soup.find('div', class_='room-details')
    if nb_joueur_label:
        nb_joueur_span = nb_joueur_label.find('span', class_='is-hidden-mobile')
        if nb_joueur_span:
            nb_joueur_text = nb_joueur_span.get_text(strip=True)
            nb_joueur = re.sub(r'\s*joueurs$', '', nb_joueur_text).strip()

    info_top_div = soup.find('div', class_='room-description')
    if info_top_div:
        paragraphs = [p.get_text(strip=True) for p in info_top_div.find_all(['p', 'br'])]
        info_top = '\n'.join([re.sub(r'(?<=[.!?])(?=[A-Z])', ' ', text) for text in paragraphs])
        info_top_formatted = format_multiline_text(info_top)
    
    figure = soup.find('figure', id='label-overview')
    if figure:
        style_attr = figure.get('style', '')
        image_url_match = re.search(r'background-image:\s*url\(\"(.*?)\"\)', style_attr)
        if image_url_match:
            image_url = image_url_match.group(1)
            #image_name = os.path.basename(image_url)
            image_name = f"{url_suffix}.webp"
            # Download and save the image
            save_dir = "../assets/img/escape/"
            os.makedirs(save_dir, exist_ok=True)  # Ensure directory exists

            # Generate the full file path
            image_path = os.path.join(save_dir, image_name)

            img_response = requests.get(image_url, stream=True)
            if img_response.status_code == 200:
                with open(image_path, 'wb') as img_file:
                    for chunk in img_response.iter_content(1024):
                        img_file.write(chunk)
        
    enseigne_tag = soup.find('a', class_='company-title nuxt-link-active')
    enseigne = ""
    if enseigne_tag:
        enseigne = enseigne_tag.get_text(strip=True)
        # Replace spaces with underscores
        enseigne = enseigne.replace(" ", "_")
        # Remove hyphens
        enseigne = enseigne.replace("-", "")
        enseigne = enseigne.replace("'", "")
        # Replace multiple underscores with a single underscore
        enseigne = re.sub(r'_+', '_', enseigne)  # Replace multiple underscores with a single underscore
        # Remove newlines
        enseigne = enseigne.replace("\n", "")
        # Remove leading/trailing underscores, if any
        enseigne = enseigne.strip('_')
    # Extract maps_location (address)
    maps_location = ""
    maps_tag = soup.find('p', class_='has-text-grey is-size-7 company-address')
    if maps_tag:
        maps_location = maps_tag.get_text(strip=True)

    # Extract phone number
    phone = ""
    phone_tag = soup.find('p', class_='has-text-grey is-size-7 company-phone-number')
    if phone_tag:
        phone = phone_tag.get_text(strip=True)

    # Extract website
    website = ""
    website_tag = soup.find('div', class_='buttons booking-block is-centered m-b-none')
    if website_tag:
        a_tag = website_tag.find('a', href=True)
        if a_tag:
            website = a_tag['href']
            # Get the base URL (domain) from the full URL
            website = get_base_url(website)
    
    enseigne_file = "../_data/enseignes.yml"
    if os.path.exists(enseigne_file):
        with open(enseigne_file, 'r', encoding='utf-8') as f:
            enseigne_data = yaml.safe_load(f) or {}
        # Check if the enseigne already exists as a key inside the 'enseignes' section
        if enseigne not in enseigne_data.get('enseignes', {}):
            # If not, append a new entry for this enseigne inside 'enseignes'
            enseigne_data.setdefault('enseignes', {})[enseigne] = {
                'name': clean_enseigne_name(enseigne_tag.get_text(strip=True)),
                'location': maps_location or 'Unknown',
                'website': website or "",
                'phone': phone or "",
                'email': "",  # Email not found
                'maps_location': ""
            }
        # Write the updated data back to the YAML file
        with open(enseigne_file, 'w', encoding='utf-8') as f:
            yaml.dump(enseigne_data, f, allow_unicode=True)
    
    
    # Markdown content
    md_content = f"""---
layout: article_not_descriptive
url: "{url_suffix}"
top_name : "{url_suffix}"
title: {title}
date: 07-06-2024
enseigne: "{enseigne}"
theme : "{theme}"
duree : "{duree}"
nb-joueur : "{nb_joueur}"
image_name : "{image_name}"
info_top : |{info_top_formatted}
---
"""
    
    # Define the save directory for articles
    articles_dir = "../_articles/"
    os.makedirs(articles_dir, exist_ok=True)  # Ensure directory exists
    
    # Write to .md file in the specified directory
    filename = os.path.join(articles_dir, f"{url_suffix}.md")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)
    
    print(f"Markdown file '{filename}' created successfully.")
    if image_name:
        print(f"Image '{image_name}' downloaded successfully.")

    ## Append the top_name at the end of top_file
    # Check if the top_name is already in the file to avoid duplicates
    top_file = "../_top-france/avignon.md"
    top_name_entry = f"- {url_suffix}\n"
    if os.path.exists(top_file):
        with open(top_file, "r", encoding="utf-8") as f:
            content = f.readlines()
        
        if top_name_entry not in content:
            with open(top_file, "a", encoding="utf-8") as f:
                f.write(top_name_entry)
            print(f"Appended '{url_suffix}' to '{top_file}'")
        else:
            print(f"'{url_suffix}' is already present in '{top_file}'")
    # else:
    #     # If the file does not exist, create it and add the entry
    #     with open(top_file, "w", encoding="utf-8") as f:
    #         f.write(top_name_entry)
    #     print(f"Created '{top_file}' and added '{url_suffix}'")

# Run function
extract_data_and_create_md()

