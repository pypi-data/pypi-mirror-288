import requests
from bs4 import BeautifulSoup
import re
import json

class GoFundMeScraper:
    def __init__(self, class_values=None, json_filename=None):
        if class_values is None:
            class_values = {
                "title": "p-campaign-title",
                "description": "p-campaign-description",
                "progress": "progress-meter_progressMeter",
                "hero_image": "campaign-hero_image",
                "creation_date": "m-campaign-byline-created"
            }
        self.class_values = class_values

        if json_filename is None:
            json_filename = 'gofundme_campaign.json'
        self.json_filename = json_filename

    def get_gofundme_details(self, url):
        # Fetch the content of the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the title element
            title_element = soup.find('h1', class_=self.class_values["title"])
            title = title_element.text.strip() if title_element else None
            
            # Find the description element
            description_element = soup.find('div', class_=self.class_values["description"])
            description = description_element.text.strip() if description_element else None
            description = description.replace("Donation protected", "")
            description = re.sub(r'\n+','\n\n', description)

            # Find the progress meter element
            progress_element = soup.find('div', class_=lambda value: value and value.startswith(self.class_values["progress"]))
            progress = progress_element.text.strip() if progress_element else None
            
            # Extract numbers using regex
            if progress:
                number_pattern = re.compile(r'[\d,]+(?:\.\d+)?[Kk]?')
                numbers = number_pattern.findall(progress)
                if len(numbers) >= 3:
                    progress_numbers = numbers[:3]
                    progress_numbers = [self.convert_to_number(num) for num in progress_numbers]
                else:
                    progress_numbers = None
            else:
                progress_numbers = None
            
            # Find the campaign hero image
            hero_image_container = soup.find('picture', class_=lambda value: value and value.startswith(self.class_values["hero_image"]))
            hero_image = hero_image_container.find('img')['src'] if hero_image_container else "https://www.hostmerchantservices.com/wp-content/uploads/2022/05/godfundme-review-1200x900.jpg"
            
            # Find the creation date element
            creation_date_element = soup.find('span', class_=self.class_values["creation_date"])
            creation_date = creation_date_element.text.strip() if creation_date_element else None
            
            return title, description, progress_numbers, hero_image, creation_date
        return None, None, None, None

    def convert_to_number(self, num_str):
        # Remove any currency symbols and commas
        num_str = num_str.replace('€', '').replace(',', '')
        
        # Convert to float or integer
        if 'K' in num_str or 'k' in num_str:
            return float(num_str.replace('K', '').replace('k', '')) * 1000
        else:
            return float(num_str) if '.' in num_str else int(num_str)
        
    def save_to_json(self, data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def get_many_gofundme_details(self, urls):
        data = []
        
        for url in urls:
            title, description, progress_numbers, hero_image, creation_date = self.get_gofundme_details(url)
            if progress_numbers:  # Check if progress_numbers is not None
                row = {
                    "icon": hero_image,
                    "title": title,
                    "description": description,
                    "receivedAmt": progress_numbers[0],
                    "totalAmt": progress_numbers[1],
                    "progressRatio": progress_numbers[0] / progress_numbers[1],
                    "creationDate": creation_date,
                    "link": url
                }
                data.append(row)

        self.save_to_json(data, self.json_filename)


