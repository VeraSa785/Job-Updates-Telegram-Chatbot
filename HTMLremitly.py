import requests
from bs4 import BeautifulSoup

class HTMLremitly:
    def __init__(self, url):
        self.url = url
        self.excluded_words = ["Principal", "Senior", "II", "III"]

    def parse_html(self):
        # Send a GET request to the URL
        response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all <tr> elements with class "grid-item"
            tr_elements = soup.select('tr.grid-item')

            # Initialize an empty list to store the job information
            job_list = []

            # Iterate over the <tr> elements
            for tr in tr_elements:
                # Extract the job title
                job_title = tr.select_one('td:nth-child(1)').get_text(strip=True)

                # Extract the department
                department_name = tr.select_one('td:nth-child(2)').get_text(strip=True)

                # Extract the location
                location_name = tr.select_one('td:nth-child(3)').get_text(strip=True)

                # Extract the job link
                job_link = tr.select_one('td:nth-child(4) a')['href']

                # Exclude jobs with "Principal" or "Senior" in the title
                if all(word not in job_title for word in self.excluded_words) and 'Software' in job_title:
                    # Create a dictionary with the job information
                    job_dict = {
                        "Job Title": job_title,
                        "Department": department_name,
                        "Location": location_name,
                        "Job Link": job_link
                    }

                    # Append the job dictionary to the list
                    job_list.append(job_dict)

            return job_list
        else:
            print("Request failed with status code:", response.status_code)
            return []

# Usage example
url = "https://careers.remitly.com/all-open-jobs/?team=engineering"
html_parser = HTMLremitly(url)
jobs = html_parser.parse_html()
for job in jobs:
    print(job)
    
