import requests
from bs4 import BeautifulSoup

# Global list of words to exclude
exclusion_words = ["Senior", "Software Engineer II"]

class HTMLParser:
    def __init__(self, url):
        self.url = url

    def parse_html(self):

        url = "https://www.smartsheet.com/careers-list?location=Bellevue%2C%20WA%2C%20USA&department=Engineering%20-%20Developers&position=&page=0"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        titles = soup.find_all("td", class_="views-field views-field-title")
        departments = soup.find_all("td", class_="views-field views-field-field-department")
        locations = soup.find_all("td", class_="views-field views-field-field-posting-location")

        job_data = []

        for title, department, location in zip(titles, departments, locations):
            job_title = title.find("a").get_text(strip=True)
            job_link = title.find("a")["href"]
            department_name = department.get_text(strip=True)
            location_name = location.get_text(strip=True)

            if any(word in job_title for word in exclusion_words):
                continue

            job_dict = {
                "Job Title": job_title,
                "Department": department_name,
                "Location": location_name,
                "Job Link": job_link
            }

            job_data.append(job_dict)

        # Print the job data
        # for job in job_data:
        #     print(job)
        #     print()

        return job_data