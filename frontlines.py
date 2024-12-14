

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

# def ensure_unique_key(jobs, job_title):
#     """Ensure unique job titles in the dictionary by appending a suffix."""
#     original_title = job_title
#     counter = 1
#     while job_title in jobs:
#         job_title = f"{original_title} ({counter})"
#         counter += 1
#     return job_title

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
#                 unique_job_title = ensure_unique_key(jobs, job_title)
#                 jobs[unique_job_title] = job_link
#         finally:
#             driver.quit()

#     # Save to JSON
#     with open('output.json', 'w') as f:
#         json.dump(jobs, f, indent=4)
#     print(f"Total jobs saved: {len(jobs)}")
#     print("Jobs saved to 'output.json'.")

# if __name__ == "__main__":
#     main()



# ---

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.common.exceptions import WebDriverException

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
            print(f"Attempt {attempt + 1} to fetch {url}")
            driver.get(url)  # Attempt to navigate to the URL
            
            # Wait for job post elements to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.entry-title.td-module-title a"))
            )
            
            # Scroll to ensure all content is loaded
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Find job post elements
            job_posts = driver.find_elements(By.CSS_SELECTOR, "h3.entry-title.td-module-title a")
            return [(post.text.strip(), post.get_attribute("href").strip()) for post in job_posts]
        
        except WebDriverException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt == retries - 1:  # On the last attempt, log the page source and re-raise
                print("Final attempt failed. Page source:")
                print(driver.page_source)
                raise
            time.sleep(5)  # Wait 5 seconds before retrying
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
