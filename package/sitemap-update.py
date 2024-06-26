import os
import datetime
import re
import xml.etree.ElementTree as ET

def generate_sitemap_index(directory, sitemap_index_path=None, tree=None, root=None):
    # Define XML namespace mapping
    ns = {'': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # Create or update existing sitemap_index.xml
    if sitemap_index_path is None:
        sitemap_index_path = os.path.join(directory, "sitemap_index.xml")
    if tree is None and os.path.exists(sitemap_index_path):
        tree = ET.parse(sitemap_index_path)
        root = tree.getroot()

    # Get existing URLs from the sitemap index
    existing_urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]

    # Iterate through HTML files in the directory
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            # If it's a directory, recursively call generate_sitemap_index
            generate_sitemap_index(os.path.join(directory, filename), sitemap_index_path, tree, root)
        elif filename.endswith(".html"):
            pattern = r'^.*?nelsonkent\.github\.io'
            new_path = re.sub(pattern, '', directory)

            file_url = f"https://nelsonkent.github.io/{filename}"
            if new_path:
                file_url = f"https://nelsonkent.github.io{new_path}/{filename}"
            print(file_url)
            if file_url not in existing_urls:
                file_path = os.path.join(directory, filename)
                last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')

                # Create sitemap entry with proper namespace
                sitemap_elem = ET.SubElement(root, "{http://www.sitemaps.org/schemas/sitemap/0.9}url")
                loc_elem = ET.SubElement(sitemap_elem, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                loc_elem.text = file_url
                lastmod_elem = ET.SubElement(sitemap_elem, "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
                lastmod_elem.text = last_modified

    if os.path.dirname(sitemap_index_path) == directory:
        # Write the updated sitemap index to file
        tree.write(sitemap_index_path, encoding="UTF-8", xml_declaration=True)

# Get the parent directory
parent_directory = os.path.dirname(os.getcwd())
# Call the function and pass the parent directory
generate_sitemap_index(parent_directory)
