import os
import re
import yaml

ARTICLES_DIR = "../_articles"
ENSEIGNES_DIR = "../enseignes"  # output folder for enseigne index pages

os.makedirs(ENSEIGNES_DIR, exist_ok=True)

enseigne_set = set()

# Regex to capture YAML front matter
front_matter_re = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

def safe_slug(text: str) -> str:
    """Make a safe-ish slug from enseigne name (spaces -> _, keep letters/numbers/_)."""
    return re.sub(r"[^A-Za-z0-9_]+", "_", text.strip())

# Process all articles
for filename in os.listdir(ARTICLES_DIR):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(ARTICLES_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = front_matter_re.match(content)
    if not match:
        print(f"⚠️ No front matter found in {filename}")
        continue

    front_matter_text = match.group(1)
    front_matter = yaml.safe_load(front_matter_text)

    # Ensure we have enseigne
    enseigne = front_matter.get("enseigne")
    if not enseigne:
        print(f"⚠️ No 'enseigne' in {filename}, skipping permalink update.")
        continue

    enseigne_set.add(enseigne)
    enseigne_slug = safe_slug(enseigne)

    # Use existing `url` field or fallback to filename (without .md)
    slug = front_matter.get("url") or os.path.splitext(filename)[0]

    # Construct permalink
    permalink = f"/{enseigne_slug}/{slug}"
    front_matter["permalink"] = permalink

    # Rewrite file with updated front matter
    new_front_matter = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
    new_content = f"---\n{new_front_matter}\n---\n" + content[match.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Updated permalink for {filename} → {permalink}")

# Generate one enseigne index page per unique enseigne
for enseigne in sorted(enseigne_set):
    enseigne_slug = safe_slug(enseigne)
    filepath = os.path.join(ENSEIGNES_DIR, f"{enseigne_slug}.md")

    front_matter = f"""---
layout: enseigne
enseigne: "{enseigne}"
permalink: /{enseigne_slug}/
title: "{enseigne}"
---
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(front_matter)

    print(f"📝 Generated {filepath}")

print("🎉 Done! Articles updated and enseigne index pages generated.")
