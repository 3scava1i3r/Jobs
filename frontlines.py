# import requests
# import json
# from bs4 import BeautifulSoup

# url = "https://frontlinesmedia.in/category/job-notifications/"
# jobs = {}  # create an empty dictionary to store job titles and links

# try:
#     for page in range(1, 4):  # scrape first 3 pages
#         page_url = url + f"page/{page}/"
#         response = requests.get(page_url)  # send a GET request to the page URL

#         # Check if the response is OK (status code 200)
#         if response.status_code != 200:
#             raise Exception(f"Failed to get page {page_url}. Status code: {response.status_code}")

#         soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content using BeautifulSoup
#         job_posts = soup.find_all('h3', class_='entry-title td-module-title')  # find all job post titles
#         for post in job_posts:
#             job_title = post.find('a').text  # extract the job title from the anchor tag
#             job_link = post.find('a')['href']  # extract the job link from the anchor tag
#             jobs[job_title] = job_link  # add the job title and link to the dictionary

#     with open('output.json', 'w') as f:
#         json.dump(jobs, f)  # save the dictionary to a JSON file

# except Exception as e:
#     print(f"Error: {e}")
    
# # End of the code

# ----

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import json

# # Set Chrome options for headless mode
# options = Options()
# options.add_argument("--headless")  # Run Chrome in headless mode
# options.add_argument("--no-sandbox")  # Required for environments like Codespaces
# options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
# options.add_argument("--disable-gpu")  # Disable GPU for headless mode
# options.add_argument("--remote-debugging-port=9222")  # Avoid debugging conflicts

# # Set up the Chrome WebDriver
# service = Service()  # Use ChromeDriver bundled with Selenium Manager
# driver = webdriver.Chrome(service=service, options=options)

# try:
#     jobs = {}
#     for page in range(1, 4):
#         url = f"https://frontlinesmedia.in/category/job-notifications/page/{page}/"
#         driver.get(url)

#         job_posts = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title.td-module-title a")
#         for post in job_posts:
#             print(job_posts,"post")
#             job_title = post.text.strip()
#             job_link = post.get_attribute("href").strip()
#             jobs[job_title] = job_link

#     # Save the job data to a JSON file
#     with open('output.json', 'w') as f:
#         json.dump(jobs, f, indent=4)

#     print("Jobs saved to 'output.json'.")
# finally:
#     driver.quit()


# ----


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import json

# options = Options()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# driver = webdriver.Chrome(options=options)

# try:
#     jobs = {}
#     for page in range(1, 4):
#         print(f"Fetching page {page}...")
#         url = f"https://frontlinesmedia.in/category/job-notifications/page/{page}/"
#         driver.get(url)

#         # Wait for elements to load
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.entry-title.td-module-title a"))
#         )

#         # Optionally scroll to ensure content is loaded
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Wait for any lazy-loaded elements

#         job_posts = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title.td-module-title a")
#         print(f"Number of job posts found: {len(job_posts)}")

#         # Extract job titles and links
#         for post in job_posts:
#             print(post)
#             job_title = post.text.strip()
#             job_link = post.get_attribute("href").strip()
#             print(f"Job: {job_title}, Link: {job_link}")
#             jobs[job_title] = job_link

#     # Save to JSON
#     with open('output.json', 'w') as f:
#         json.dump(jobs, f, indent=4)
#         print("Jobs saved to 'output.json'.")
# finally:
#     driver.quit()


# ---
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import json

# options = Options()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# driver = webdriver.Chrome(options=options)

# try:
#     jobs = {}
#     for page in range(1, 4):
#         print(f"Fetching page {page}...")
#         url = f"https://frontlinesmedia.in/category/job-notifications/page/{page}/"
#         driver.get(url)

#         # Wait for elements to load or timeout after 20 seconds
#         try:
#             WebDriverWait(driver, 20).until(
#                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.entry-title.td-module-title a"))
#             )
#         except Exception as e:
#             print(f"Error on page {page}: {e}")
#             print("Page source for debugging:")
#             print(driver.page_source)  # Debugging: Print the HTML content
#             continue  # Skip to the next page

#         # Scroll to ensure all content is loaded
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)

#         # Find job post elements
#         job_posts = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title.td-module-title a")
#         print(f"Number of job posts found on page {page}: {len(job_posts)}")

#         # Extract job titles and links
#         for post in job_posts:
#             job_title = post.text.strip()
#             job_link = post.get_attribute("href").strip()
#             print(f"Job: {job_title}, Link: {job_link}")
#             jobs[job_title] = job_link

#     # Save to JSON
#     with open('output.json', 'w') as f:
#         json.dump(jobs, f, indent=4)
#         print("Jobs saved to 'output.json'.")
# finally:
#     driver.quit()

# ---

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import json

# def setup_driver():
#     """Set up and return a Selenium WebDriver instance."""
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
#     driver = webdriver.Chrome(options=options)
#     driver.implicitly_wait(10)  # Set an implicit wait
#     return driver

# def fetch_job_posts(driver, url, retries=3):
#     """Fetch job posts from a given URL with retries."""
#     for attempt in range(retries):
#         try:
#             driver.get(url)
#             WebDriverWait(driver, 20).until(
#                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.entry-title.td-module-title a"))
#             )
#             # Scroll to ensure all content is loaded
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)
            
#             # Find job post elements
#             job_posts = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title.td-module-title a")
#             return [(post.text.strip(), post.get_attribute("href").strip()) for post in job_posts]
#         except Exception as e:
#             print(f"Attempt {attempt + 1} failed for {url}: {e}")
#             if attempt == retries - 1:  # On the last attempt, log page source
#                 print("Final attempt failed. Page source:")
#                 print(driver.page_source)
#     return []

# def main():
#     driver = setup_driver()
#     try:
#         jobs = {}
#         for page in range(1, 4):
#             print(f"Fetching page {page}...")
#             url = f"https://frontlinesmedia.in/category/job-notifications/page/{page}/"
#             job_posts = fetch_job_posts(driver, url)
#             print(f"Number of job posts found on page {page}: {len(job_posts)}")
            
#             for job_title, job_link in job_posts:
#                 print(f"Job: {job_title}, Link: {job_link}")
#                 jobs[job_title] = job_link

#         # Save to JSON
#         with open('output.json', 'w') as f:
#             json.dump(jobs, f, indent=4)
#             print("Jobs saved to 'output.json'.")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()






# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import json

# def setup_driver(user_agent):
#     """Set up and return a Selenium WebDriver instance with a specific user agent."""
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument(f"--user-agent={user_agent}")
    
#     driver = webdriver.Chrome(options=options)
#     driver.implicitly_wait(10)  # Set an implicit wait
#     return driver

# def fetch_job_posts(driver, url, retries=3):
#     """Fetch job posts from a given URL with retries."""
#     for attempt in range(retries):
#         try:
#             driver.get(url)
#             WebDriverWait(driver, 20).until(
#                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.entry-title.td-module-title a"))
#             )
#             # Scroll to ensure all content is loaded
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)
            
#             # Find job post elements
#             job_posts = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title.td-module-title a")
#             return [(post.text.strip(), post.get_attribute("href").strip()) for post in job_posts]
#         except Exception as e:
#             print(f"Attempt {attempt + 1} failed for {url}: {e}")
#             if attempt == retries - 1:  # On the last attempt, log page source
#                 print("Final attempt failed. Page source:")
#                 print(driver.page_source)
#     return []

# def main():
#     user_agents = [
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0"
#     ]

#     jobs = {}
#     for page in range(1, 4):
#         user_agent = user_agents[page % len(user_agents)]  # Cycle through user agents
#         print(f"Fetching page {page} with user agent: {user_agent}")
        
#         driver = setup_driver(user_agent)
#         try:
#             url = f"https://frontlinesmedia.in/category/job-notifications/page/{page}/"
#             job_posts = fetch_job_posts(driver, url)
#             print(f"Number of job posts found on page {page}: {len(job_posts)}")
            
#             for job_title, job_link in job_posts:
#                 print(f"Job: {job_title}, Link: {job_link}")
#                 jobs[job_title] = job_link
#         finally:
#             driver.quit()

#     # Save to JSON
#     with open('output.json', 'w') as f:
#         json.dump(jobs, f, indent=4)
#         print("Jobs saved to 'output.json'.")

# if __name__ == "__main__":
#     main()









from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def setup_driver(user_agent):
    """Set up and return a Selenium WebDriver instance with a specific user agent."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-agent={user_agent}")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # Set an implicit wait
    return driver

def fetch_job_posts(driver, url, retries=3):
    """Fetch job posts from a given URL with retries."""
    for attempt in range(retries):
        try:
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.entry-title.td-module-title a"))
            )
            # Scroll to ensure all content is loaded
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Find job post elements
            job_posts = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title.td-module-title a")
            return [(post.text.strip(), post.get_attribute("href").strip()) for post in job_posts]
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt == retries - 1:  # On the last attempt, log page source
                print("Final attempt failed. Page source:")
                print(driver.page_source)
    return []

def ensure_unique_key(jobs, job_title):
    """Ensure unique job titles in the dictionary by appending a suffix."""
    original_title = job_title
    counter = 1
    while job_title in jobs:
        job_title = f"{original_title} ({counter})"
        counter += 1
    return job_title

def main():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0"
    ]

    jobs = {}
    for page in range(1, 4):
        user_agent = user_agents[page % len(user_agents)]  # Cycle through user agents
        print(f"Fetching page {page} with user agent: {user_agent}")
        
        driver = setup_driver(user_agent)
        try:
            url = f"https://frontlinesmedia.in/category/job-notifications/page/{page}/"
            job_posts = fetch_job_posts(driver, url)
            print(f"Number of job posts found on page {page}: {len(job_posts)}")
            
            for job_title, job_link in job_posts:
                unique_job_title = ensure_unique_key(jobs, job_title)
                jobs[unique_job_title] = job_link
        finally:
            driver.quit()

    # Save to JSON
    with open('output.json', 'w') as f:
        json.dump(jobs, f, indent=4)
    print(f"Total jobs saved: {len(jobs)}")
    print("Jobs saved to 'output.json'.")

if __name__ == "__main__":
    main()
