import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib.parse import urlparse, urljoin

# ANSI color codes for terminal output
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'

# Function to print a banner
def print_banner():
    banner = """
    ████████╗██████╗ ██╗   ██╗██╗     ██╗███████╗██████╗ 
    ╚══██╔══╝██╔══██╗██║   ██║██║     ██║██╔════╝██╔══██╗
       ██║   ██████╔╝██║   ██║██║     ██║█████╗  ██████╔╝
       ██║   ██╔══██╗██║   ██║██║     ██║██╔══╝  ██╔══██╗
       ██║   ██║  ██║╚██████╔╝███████╗██║███████╗██║  ██║
       ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝
    """
    print(colors.GREEN + banner + colors.END)

# Function to fetch HTML content of a URL
def fetch_html(url):
    response = requests.get(url)
    return response.text

# Function to save content to a file
def save_content(content, filename):
    with open(filename, 'wb') as file:
        file.write(content)

# Function to download resources (CSS, JavaScript, images, etc.)
def download_resources(url, content, output_dir):
    soup = BeautifulSoup(content, 'html.parser')

    # Find all tags that may contain resource URLs
    resource_tags = soup.find_all(['link', 'script', 'img'])

    for tag in resource_tags:
        if tag.name == 'link' and tag.get('href'):
            resource_url = urljoin(url, tag['href'])
            tag['href'] = os.path.relpath(os.path.join(output_dir, os.path.basename(urlparse(resource_url).path)), os.path.dirname(os.path.join(output_dir, 'index.html')))
        elif tag.name == 'script' and tag.get('src'):
            resource_url = urljoin(url, tag['src'])
            tag['src'] = os.path.relpath(os.path.join(output_dir, os.path.basename(urlparse(resource_url).path)), os.path.dirname(os.path.join(output_dir, 'index.html')))
        elif tag.name == 'img' and tag.get('src'):
            resource_url = urljoin(url, tag['src'])
            tag['src'] = os.path.relpath(os.path.join(output_dir, os.path.basename(urlparse(resource_url).path)), os.path.dirname(os.path.join(output_dir, 'index.html')))

        # Get the filename of the resource
        resource_filename = os.path.join(output_dir, os.path.basename(urlparse(resource_url).path))

        # Download and save the resource
        try:
            response = requests.get(resource_url)
            if response.status_code == 200:
                save_content(response.content, resource_filename)
                print(f"{colors.GREEN}Downloaded:{colors.END} {resource_url}")
            else:
                print(f"{colors.RED}Failed to download:{colors.END} {resource_url}")
        except Exception as e:
            print(f"{colors.RED}Failed to download:{colors.END} {resource_url} - {e}")

    return str(soup)

# Main function to clone website
def clone_website(url, output_dir):
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Prepend "http://" if no scheme is provided
        if not urlparse(url).scheme:
            url = "http://" + url

        # Fetch HTML content
        html_content = fetch_html(url)

        # Save HTML content to a file
        html_filename = os.path.join(output_dir, 'index.html')
        html_content_with_local_paths = download_resources(url, html_content, output_dir)
        save_content(html_content_with_local_paths.encode('utf-8'), html_filename)

        print("Website cloned successfully!")
    except KeyboardInterrupt:
        print(f"{colors.GREEN}Goodbye! You exited.{colors.END}")
        sys.exit()

if __name__ == "__main__":
    print_banner()
    # Accept user input for URL and output directory
    url = input("Enter the website URL: ")
    output_directory = input("Enter the output directory path: ")

    # Clone the website
    clone_website(url, output_directory)
