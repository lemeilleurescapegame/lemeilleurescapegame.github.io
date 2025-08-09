import requests
from bs4 import BeautifulSoup
import re
import os

def find_similar_section_text(soup, required_classes):
    """
    Finds the first <section> that contains all the required class names (ignoring unique parts).
    Returns the section text.
    """
    sections = soup.find_all("section")
    for section in sections:
        section_classes = section.get("class", [])  # Get all classes as a list

        if section_classes and all(cls in section_classes for cls in required_classes):
            return section.get_text(separator="\n", strip=True)  # Extract text
    return ""

def find_resenti_global(soup):
    """
    Finds the 'Ressenti global' section and extracts the text from the
    next 'elementor-text-editor elementor-clearfix' div.
    """
    # Find the heading containing "Ressenti global"
    resenti_heading = soup.find("div", class_="elementor-text-editor elementor-clearfix", 
                                string=lambda text: text)
    if not resenti_heading:
        return "NO 'Ressenti global' FOUND"
    
    # Find the section containing this heading
    resenti_section = resenti_heading.find_parent("section")
    
    if not resenti_section:
        return "NO SECTION FOUND FOR 'Ressenti global'"

    # Find the next section after this one
    next_section = resenti_section.find_next_sibling("section")
    
    if not next_section:
        return "NO NEXT SECTION FOUND AFTER 'Ressenti global'"

    # Extract text from the first 'elementor-text-editor elementor-clearfix' div inside the next section
    resenti_div = next_section.find("div", class_="elementor-text-editor elementor-clearfix")
    
    if not resenti_div:
        return "NO TEXT DIV FOUND AFTER 'Ressenti global'"

    return resenti_div.get_text(separator="\n", strip=True)

def extract_data_and_create_md():
    url = input("Enter the URL: ")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract last part of URL
    url_suffix = url.rstrip('/').split('/')[-1]
    
    # Extract title
    title_tag1 = soup.find('h1', class_='elementor-heading-title elementor-size-xl')
    title_tag2 = soup.find('h1', class_='elementor-heading-title elementor-size-default')
    title = title_tag1.get_text(strip=True) if title_tag1 else title_tag2.get_text(strip=True) if title_tag2 else ""
    
    # Extract note and keep only the first number
    note_tag = soup.find('span', class_='premium-title-text')
    note = note_tag.get_text(strip=True) if note_tag else ""
    note_match = re.search(r'\d+', note)
    note = note_match.group(0) if note_match else ""
    
    # Extract theme, duree, and nb-joueur
    theme = duree = nb_joueur = ""
    
    icon_boxes = soup.find_all('h4', class_='elementor-icon-box-title')
    for box in icon_boxes:
        box_text = box.get_text(strip=True)
        if "Thème" in box_text:
            theme_description = box.find_next('p', class_='elementor-icon-box-description')
            if theme_description:
                theme = theme_description.get_text(strip=True)
        elif "Durée" in box_text or "Temps" in box_text:
            duree_description = box.find_next('p', class_='elementor-icon-box-description')
            if duree_description:
                duree = duree_description.get_text(strip=True)
        elif "Nombre de joueurs" in box_text:
            nb_joueur_description = box.find_next('p', class_='elementor-icon-box-description')
            if nb_joueur_description:
                nb_joueur = nb_joueur_description.get_text(strip=True)

    # Extract author
    author_tag = soup.find('div', class_='saboxplugin-authorname')
    author = author_tag.get_text(strip=True) if author_tag else ""
    

    # elementor-section 
    # elementor-top-section 
    # elementor-element 
    # elementor-element-b41c9d1 
    # elementor-section-content-middle 
    # elementor-section-boxed 
    # elementor-section-height-default 
    # elementor-section-height-default

    # Extract scenario (similar flexible approach)
    scenario = find_similar_section_text(soup, [
        "elementor-section", 
        "elementor-top-section", 
        "elementor-section-content-middle", 
        "elementor-section-boxed", 
        "elementor-section-height-default"
    ])
    
    # Remove "Le scénario :" from the beginning of the scenario
    scenario = re.sub(r'^Le scénario\s*:\s*', '', scenario)

    # Format scenario and resenti_global with consistent indentation
    def format_multiline_text(text):
        return "\n    " + "\n    ".join(text.split("\n")) if text else ""
    

    scenario_formatted = format_multiline_text(scenario)
    
    # elementor-section 
    # elementor-top-section 
    # elementor-element 
    # elementor-element-dfab133 
    # elementor-section-boxed 
    # elementor-section-height-default 
    # elementor-section-height-default

    # Extract resenti_global (using a flexible approach)
    resenti_global = find_similar_section_text(soup, [
        "elementor-section", 
        "elementor-top-section",
        "elementor-section-boxed",
        "elementor-section-height-default"
    ])
    #resenti_global = find_resenti_global(soup)

    #print('## -> ' , resenti_global)
    resenti_global_formatted = format_multiline_text(resenti_global)
    
    # Markdown content
    md_content = f"""---
layout: article
url: "{url_suffix}"
top_name : "{url_suffix}"
title: "{title}"
date: 07-06-2024
note: "{note}"
enseigne: ""
theme : "{theme}"
duree : "{duree}"
nb-joueur : "{nb_joueur}"
redacteur : "{author}"
image_name : ""
scenario : |{scenario_formatted}
resenti_global : |{resenti_global_formatted}
---
"""
    
    # Write to .md file
    articles_dir = "../_articles/"
    os.makedirs(articles_dir, exist_ok=True)  # Ensure directory exists

    filename = os.path.join(articles_dir, f"{url_suffix}.md")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)
    
    print(f"Markdown file '{filename}' created successfully.")

# Run function
extract_data_and_create_md()

