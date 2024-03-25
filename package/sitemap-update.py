import os
import datetime
import xml.etree.ElementTree as ET

def generate_sitemap_index(directory, sitemap_index_path=None, tree=None, root=None):
    # Create or update existing sitemap_index.xml
    if sitemap_index_path is None:
        sitemap_index_path = os.path.join(directory, "sitemap_index.xml")
    if tree is None and os.path.exists(sitemap_index_path):
        tree = ET.parse(sitemap_index_path)
        root = tree.getroot()
    # Get existing URLs from the sitemap index
    existing_urls = [elem.text for elem in root.findall("{*}sitemap/{*}loc")]
#     print(existing_urls)

    # Iterate through HTML files in the directory
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            # If it's a directory, recursively call generate_sitemap_index
            generate_sitemap_index(os.path.join(directory, filename), sitemap_index_path, tree, root)
        elif filename.endswith(".html"):
            file_url = f"https://metabyte.cloudns.be/{filename}"
            if file_url not in existing_urls:
                file_path = os.path.join(directory, filename)
                last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')

                # Create sitemap entry
                sitemap_elem = ET.SubElement(root, "sitemap")
                loc_elem = ET.SubElement(sitemap_elem, "loc")
                loc_elem.text = file_url
                print(file_url)
                lastmod_elem = ET.SubElement(sitemap_elem, "lastmod")
                lastmod_elem.text = last_modified

    if os.path.dirname(sitemap_index_path) == directory:
        # Write the updated sitemap index to file
        tree.write(sitemap_index_path, encoding="UTF-8", xml_declaration=False)

# Get the parent directory
parent_directory = os.path.dirname(os.getcwd())
# Call the function and pass the parent directory
generate_sitemap_index(parent_directory)
