from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import logging
import re
import os
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/task_assign_script.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Retrieve environment variables
username = os.getenv('username')
password = os.getenv('password')
project_link = os.getenv('project_link')
chrome_driver_path = os.getenv('chrome_driver')
ids_paths = os.getenv('ids_paths')
starting_email="vi@in.com"

# Validate environment variables
if not all([username, password, project_link, chrome_driver_path, ids_paths]):
    raise ValueError("Some environment variables are missing.")

# Open the JSON file and load its contents
with open(ids_paths, 'r') as file:
    data = json.load(file)

# # Path to your ChromeDriver executable
# service = Service(executable_path=chrome_driver)

# # Create a WebDriver instance
# driver = webdriver.Chrome(service=service)
# Set up Chrome options
opt = Options()
opt.add_experimental_option("debuggerAddress", "localhost:9898")

# Create a Service object
service = Service(executable_path=chrome_driver_path)

# Create a WebDriver instance
driver = webdriver.Chrome(service=service, options=opt)
driver.maximize_window()

def login():
    try:
        logging.info("Loging to the website")
        driver.get("https://notlabel-studio.toloka-test.ai")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
        
        input_username = driver.find_element(By.ID, "email")
        input_username.send_keys(username + Keys.TAB)
        
        input_password = driver.find_element(By.ID, "password")
        input_password.send_keys(password)
        
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
    except Exception as e:
        logging.error(f"Login failed: {e}")
        print(f"Login failed: {e}")
        driver.quit()
        exit()

def open_project_link():
    logging.info("Opening the website")
    driver.get(project_link)
    time.sleep(15)

# Fetching first id
def fetch_first_id():
    seed_div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[3]/div[1]/div[2]/div/div/div[2]/div'))
    )
    first_id = seed_div_element.get_attribute('innerText')
    return int(first_id)

# Adding the id filter using is_between functionality
def add_isbetween_filter():
    add_filter_btn = driver.find_element(By.CSS_SELECTOR, "button[type='primary']")
    add_filter_btn.click()

    assign_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div/div[1]/div[12]/div/div/div[1]/div"))
    )
    assign_filter.click()

    select_id_filter  = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[29]/div/div/div[2]/div[15]/div"))
    )
    select_id_filter.click()

    assign_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div/div[1]/div[13]/div/div"))
    )
    assign_filter.click()

    select_isbetween_id  = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[30]/div/div[7]"))
    )
    select_isbetween_id.click()

# Remove the id filter using is_between functionality
def remove_isbetween_filter():
    remove_filter = driver.find_element(By.XPATH, "/html/body/div[12]/div/div[1]/div[15]/button/span")
    remove_filter.click()

def add_min_max(id, fixed_cnt, changing_cnt):
    # Adding min value
    input_element = driver.find_element(By.XPATH, "/html/body/div[12]/div/div[1]/div[14]/input[1]")
    input_element.clear()
    input_element.send_keys(id)

    # Adding max value by adding the cnt variable  
    input_element = driver.find_element(By.XPATH, "/html/body/div[12]/div/div[1]/div[14]/input[2]")
    input_element.clear()
    last_id = id+changing_cnt-1
    input_element.send_keys(last_id)

    time.sleep(2)

    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/div[2]/div/img"))
    )

    seed_div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div/span/div/span[1]'))
    )
    span_text = seed_div_element.get_attribute('innerText')
    
    match = re.search(r'Tasks:\s*(\d+)\s*/\s*\d+', span_text)
    if match:
        tasks_completed = int(match.group(1))
        if tasks_completed < fixed_cnt:
            changing_cnt = changing_cnt + (fixed_cnt - tasks_completed)
            return add_min_max(id, fixed_cnt, changing_cnt)

    return changing_cnt

def assign_to_annotator(toloka_id):
    # Select Button to select all the tasks
    select_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div/span/input")
    select_btn.click()
    
    action_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/button[1]")
    action_btn.click()
    
    # Button for assign to annotator
    assign_annotator_btn = driver.find_element(By.XPATH, "/html/body/div[4]/ul/li[1]/div")
    assign_annotator_btn.click()
    
    # Wait for the cancel button to become visible
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[32]/div/div/div[2]/div/div[2]/div/button[1]"))
    )

    # Put toloka id into the search input
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[32]/div/div/div[2]/div/div[1]/div[1]/div[2]/label/div[2]/input"))
    )
    search_input.send_keys(toloka_id)
    
    # Move the id from the member to be assigned
    select_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[32]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/label/div[1]/div/span/input"))
    )
    select_btn.click()
    
    time.sleep(1)
    move_btn = driver.find_element(By.XPATH, "/html/body/div[32]/div/div/div[2]/div/div[1]/div[2]/div/button[1]")
    move_btn.click()
    
    select_btn = driver.find_element(By.XPATH, "/html/body/div[32]/div/div/div[2]/div/div[1]/div[3]/div[2]/div/label/div[1]/div/span/input")
    select_btn.click()

    time.sleep(1)
    # Cancel button
    cancel_btn = driver.find_element(By.XPATH, "/html/body/div[32]/div/div/div[2]/div/div[2]/div/button[1]")
    cancel_btn.click()

    # TODO: Remove this part or comment it out
    select_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div/span/input")
    select_btn.click()

    # Assign button
    # assign_btn = driver.find_element(By.XPATH, "/html/body/div[32]/div/div/div[2]/div/div[2]/div/button[2]")
    # assign_btn.click()

def filter_button_click():
    filter_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/button[3]"))
    )
    filter_button.click()

def assign_tasks(toloka_id, cnt):
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/div[2]/div/img"))
    )
    time.sleep(2)
    filter_button_click()
    # Adding the id filter using is_between functionality
    add_isbetween_filter()

    # Fetching first id present in the table
    id = fetch_first_id()

    # Adding parameter into the input box 
    changing_cnt = add_min_max(id, cnt, cnt)
    filter_button_click()
    
    assign_to_annotator(toloka_id)

    print(f"Successfully assigned {cnt} tasks to {toloka_id}: {id} - {(id+changing_cnt-1)}")
    logging.info(f"Successfully assigned {cnt} tasks to {toloka_id}: {id} - {(id+changing_cnt-1)}")

    filter_button_click()
    remove_isbetween_filter()
    filter_button_click()

def main_task():
    try:
        # login()
        # open_project_link()     

        start_processing = False
        for id, cnt in data.items():
            if not start_processing:
                if id == starting_email:
                    start_processing = True
                else:
                    continue

            if float(cnt) > 0:  # Check if the value is greater than 0
                assign_tasks(id, int(cnt))
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        driver.quit()
    finally:
        logging.info("Closing the browser")
        time.sleep(1)
        driver.quit()

main_task()