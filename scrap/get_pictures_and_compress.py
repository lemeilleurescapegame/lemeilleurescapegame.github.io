import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io

# Ask the user to enter the URL
url = input("Enter the URL: ").strip()  # Get input and remove unnecessary spaces

# url = 'https://lemeilleurescapegame.fr/charat-trap-game-antenna-palace/'
# url = 'https://lemeilleurescapegame.fr/paris-wolf-gang/'
name_escape = url.rstrip('/').split('/')[-1]

# Fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all div elements with the specified class
divs = soup.find_all("div", class_="entry-thumbnail")  # Replace with actual class name
# Create a folder to save images
os.makedirs("downloaded_images", exist_ok=True)

# Initialize total saved space
total_saved = 0
total_original_size = 0
total_compressed_size = 0

divs2 = soup.find_all("div", class_="premium-banner-ib premium-banner-min-height premium-banner-premium_banner_animation2 none active")  # Replace with actual class name

# Loop through each div to find images inside
for i, div in enumerate(divs2):

    img_tag = div.find("img")  # Find <img> tag inside the div
    if img_tag and img_tag.get("src"):
        img_url = img_tag["src"]  # Get the image URL
        if not img_url.startswith("http"):  # Handle relative URLs
            img_url = url + img_url  # Adjust accordingly

        # Download the image
        img_data = requests.get(img_url).content
        img_name = f"{name_escape}.jpg"  # Save as image_0.jpg, image_1.jpg, etc.
        
        # Save the original image
        # with open(img_name, "wb") as img_file:
        #     img_file.write(img_data)
        # print(f"Downloaded: {img_name}")

        # Convert the image to .webp and save it
        original_size = len(img_data)  # Original size before compression
        img = Image.open(io.BytesIO(img_data))

        save_dir = "../assets/img/escape/"
        os.makedirs(save_dir, exist_ok=True)  # Ensure directory exists
        webp_img_name = img_name.replace(".jpg", ".webp")
        image_path = os.path.join(save_dir, webp_img_name)
        

        # Save image as .webp format with compression
        img.save(image_path, "WEBP", quality=80)  # Compress to WebP format

        os.chdir(save_dir)
        # Get the size of the compressed .webp image
        compressed_size = os.path.getsize(webp_img_name)

        # Calculate space saved
        saved_space = original_size - compressed_size
        total_saved += saved_space
        total_original_size += original_size
        total_compressed_size += compressed_size

        # Calculate and print percentage of space saved for this image
        percentage_saved = (saved_space / original_size) * 100
        print(f"Converted to {webp_img_name}. Saved {saved_space / 1024:.2f} KB ({percentage_saved:.2f}% saved)")

# Calculate and print total space saved in percentage
total_percentage_saved = (total_saved / total_original_size) * 100
print(f"\nTotal space saved: {total_saved / 1024:.2f} KB ({total_percentage_saved:.2f}% saved)")
print("All images downloaded and converted!")
