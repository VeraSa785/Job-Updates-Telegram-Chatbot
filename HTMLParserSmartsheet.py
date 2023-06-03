import requests
from bs4 import BeautifulSoup

class HTMLParserSmartsheet:
    def __init__(self, url):
        self.url = url
        self.exclusion_words = ["Senior", "II", "III", "Manager", "Principal"]

    def parse_html(self):
        # Send a GET request to the URL
        response = requests.get(self.url)
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        titles = soup.find_all("td", class_="views-field views-field-title")
        departments = soup.find_all("td", class_="views-field views-field-field-department")
        locations = soup.find_all("td", class_="views-field views-field-field-posting-location")

        job_data = []

        for title, department, location in zip(titles, departments, locations):
            # Extract the job title
            job_title = title.find("a").get_text(strip=True)
            # Extract the job link
            job_link = title.find("a")["href"]
            # Extract the department
            department_name = department.get_text(strip=True)
            # Extract the location
            location_name = location.get_text(strip=True)

            # Exclude jobs with "Principal", "Senior" and more word in the title
            if any(word in job_title for word in self.exclusion_words):
                continue

            # Create a dictionary with the job information
            job_dict = {
                "Job Title": job_title,
                "Department": department_name,
                "Location": location_name,
                "Job Link": job_link
            }
            
            # Append the job dictionary to the list
            job_data.append(job_dict)

        return job_data
    