import os
import yaml

ARTICLES_DIR = "_articles"  # adjust if needed

def remove_permalink_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return False  # no front matter

    # split front matter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    _, front_matter_raw, body = parts
    front_matter = yaml.safe_load(front_matter_raw)

    if not isinstance(front_matter, dict):
        return False

    # remove permalink if present
    if "permalink" in front_matter:
        del front_matter["permalink"]

        # rebuild file
        new_content = "---\n"
        new_content += yaml.dump(front_matter, sort_keys=False)
        new_content += "---\n"
        new_content += body.lstrip("\n")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✔ Removed permalink from {filepath}")
        return True

    return False

def process_articles(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md") or filename.endswith(".markdown"):
            remove_permalink_from_file(os.path.join(directory, filename))

if __name__ == "__main__":
    process_articles(ARTICLES_DIR)

