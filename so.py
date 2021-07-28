import requests
from bs4 import BeautifulSoup

# LIMIT = 10 #페이지당 10개의 직업이 나옴
URL = f"https://stackoverflow.com/jobs?q=python"

result = {}


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    result = {}
    title = html.find("h2", {"class": "mb4 fc-black-800 fs-body3"})
    if title:
        title = title.get_text(strip=True)
        result['title'] = title
    # company and location tags -> involved None
    comlo = html.find(
        "h3", {"class": "fc-black-700 fs-body1 mb4"})
    if comlo:
        company, location = comlo.find_all("span", recursive=False)
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        result['company'] = company
        result['location'] = location
    if result:
        return result


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        jobs_class = soup.find_all(
            "div", {"class": "d-flex"})
        # com_class = soup.find_all("h3", {"class": "fc-black-700 fs-body1 mb4"})
        for job_class in jobs_class:
            extract_job(job_class)
        # jobs.append(job_class.get_text(strip=True))

    # print(jobs)


def get_jobs():
    last_page = get_last_page()
    return []
