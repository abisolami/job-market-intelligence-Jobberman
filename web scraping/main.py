from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

jobs = []

base_url = 'https://www.jobberman.com/jobs?page='

# iterating through pages
for page in range(1, 222): #total number of pages
    print(f"Scraping page {page}...")

    url = base_url + str(page)
    # using request method
    html_txt = requests.get(url).text
    soup = BeautifulSoup(html_txt, 'lxml')

    # scraping each jobs details in the jobbermann website
    for job_info in soup.find_all('div', class_="flex flex-wrap col-span-1 mb-5 bg-white rounded-lg border border-gray-300 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-gray-500"):

        try:
            # listings page
            job_name_tag = job_info.find('p', class_='text-lg font-medium break-words text-link-500')
            job_name = job_name_tag.text.strip() if job_name_tag else None

            link_tag = job_info.find('a', attrs={'data-cy': 'listing-title-link'})
            link = link_tag['href'] if link_tag else None

            company_tag = job_info.find('p', class_='text-sm text-blue-700 text-loading-animate inline-block mt-3')
            company_name = company_tag.text.strip() if company_tag else None

            # handle spans — some jobs may have fewer than 3
            spans = job_info.find_all('span', class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide text-gray-700')
            location = spans[0].text.strip() if len(spans) > 0 else None
            job_type = spans[1].text.strip() if len(spans) > 1 else None
            salary = spans[2].text.strip() if len(spans) > 2 else None

            category_tag = job_info.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block')
            category = category_tag.text.strip() if category_tag else None

            date_tag = job_info.find('p', class_='text-sm font-normal text-gray-700 text-loading-animate')
            date_posted = date_tag.text.strip() if date_tag else None

            desc_tag = job_info.find('p', class_='text-sm font-normal text-gray-700 md:text-gray-500 md:pl-5')
            description = desc_tag.text.strip() if desc_tag else None

            # individual job page
            responsibilities = None
            requirements = None
            remuneration = None
            min_qualification = None
            experience_level = None
            experience_length = None

            if link:
                job_detail = requests.get(link).text
                job_soup = BeautifulSoup(job_detail, 'lxml')

                # responsibilities and requirements
                unordered_list = job_soup.find_all('ul', class_='list-disc list-inside')
                if len(unordered_list) > 0:
                    responsibilities = [li.get_text(strip=True) for li in unordered_list[0].find_all('li')]
                if len(unordered_list) > 1:
                    requirements = [li.get_text(strip=True) for li in unordered_list[1].find_all('li')]

                # remuneration or salary
                remuneration_tag = job_soup.find('p', string=lambda x: x and 'Remuneration' in x)
                remuneration = remuneration_tag.get_text(strip=True) if remuneration_tag else None

                #other fields
                extra = job_soup.find_all('span', class_='text-sm leading-5 font-normal text-gray-800 md:text-base md:leading-6 ml-1')
                min_qualification = extra[0].get_text(strip=True) if len(extra) > 0 else None
                experience_level = extra[1].get_text(strip=True) if len(extra) > 1 else None
                experience_length = extra[2].get_text(strip=True) if len(extra) > 2 else None

            # storing in a dictionary
            jobs.append({
                'job_title': job_name,
                'website': url,
                'company': company_name,
                'location': location,
                'working_hour': job_type,
                'salary_range': salary,
                'job_category': category,
                'date_posted': date_posted,
                'minimum_qualification': min_qualification,
                'experience_level': experience_level,
                'experience_length': experience_length,
                'remuneration': remuneration,
                'job_summary': description,
                'responsibilities': responsibilities,
                'requirement': requirements
            })

        except Exception as e:
            # If anything goes wrong on a specific job, log it and move on
            print(f"Skipped a job due to error: {e}")
            continue

    time.sleep(2)
# converting the dictionary into a dataframe
data = pd.DataFrame(jobs)
data.to_csv('jobberman_jobs.csv', index=False)
print(f"Scraped {len(data)} jobs successfully")
