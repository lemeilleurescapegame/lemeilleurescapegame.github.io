import os
import requests
from bs4 import BeautifulSoup
import re

def format_multiline_text(text):
        return "\n    " + "\n    ".join(text.split("\n")) if text else ""

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
            image_name = os.path.basename(image_url)
            
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

    
    
    # Markdown content
    md_content = f"""---
layout: article_not_descriptive
url: "{url_suffix}"
top_name : "{url_suffix}"
title: {title}
date: 07-06-2024
enseigne: ""
theme : "{theme}"
duree : "{duree}"
nb-joueur : "{nb_joueur}"
image_name : "{image_name}"
info_top : |{info_top_formatted}
---
"""
    
    # # Write to .md file
    # filename = f"{url_suffix}.md"
    # with open(filename, 'w', encoding='utf-8') as file:
    #     file.write(md_content)
    
    # print(f"Markdown file '{filename}' created successfully.")
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

# Run function
extract_data_and_create_md()
