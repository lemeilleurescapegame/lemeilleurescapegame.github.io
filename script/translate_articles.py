import os
import yaml
import re
from gpt4all import GPT4All

# === Config ===
source_folder = '../_articles'
target_folder = '../_articles_en'
model_file = "/Users/pldelacour/Library/Application Support/nomic.ai/GPT4All/mistral-7b-instruct-v0.1.Q4_0.gguf"

os.makedirs(target_folder, exist_ok=True)

# === Initialize GPT4All safely ===
model = GPT4All(model_file, allow_download=False)

# === Helper function ===
def translate_text(model, prompt):
    try:
        output = model.generate(prompt, max_tokens=2048).strip()
        return output
    except Exception as e:
        print(f"[ERROR] Translation failed: {e}")
        return ""

# === Process a single file ===
def process_file(filepath, model):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML front matter and article body
        match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if not match:
            print(f"[SKIP] No YAML block in {filepath}")
            return

        yaml_content, article_body = match.groups()
        data = yaml.safe_load(yaml_content)

        if data.get('layout') != 'article':
            print(f"[SKIP] Not an article layout in {filepath}")
            return

        # Translate YAML fields
        fields_to_translate = ['title', 'scenario', 'resenti_global', 'theme']
        for field in fields_to_translate:
            if field in data and data[field]:
                prompt = f"Translate to English:\n{data[field]}"
                translated = translate_text(model, prompt)
                if translated:
                    data[field] = translated

        # Translate entire article body
        prompt_body = f"Translate the following article from French to English:\n{article_body}"
        translated_body = translate_text(model, prompt_body)

        # Rebuild translated content
        translated_content = f"---\n{yaml.dump(data, allow_unicode=True)}---\n\n{translated_body}"

        # Save the translated file
        new_filename = os.path.join(target_folder, os.path.basename(filepath))
        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"[OK] Translated and saved: {os.path.basename(filepath)}")

    except Exception as e:
        print(f"[ERROR] Failed to process {filepath}: {e}")

# === Process all files ===
with model:
    files = [f for f in os.listdir(source_folder) if f.endswith(('.md', '.html'))]
    print(f"Found {len(files)} articles to process.")
    for filename in files:
        filepath = os.path.join(source_folder, filename)
        process_file(filepath, model)

print("[DONE] All articles processed.")
