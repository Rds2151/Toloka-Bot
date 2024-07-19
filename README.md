# Toloka-Bot

## Selenium Automation Script for Task Assignment

## Overview

This repository contains a Python script that automates task assignments using Selenium WebDriver. The script:

- Reads a JSON file with email IDs and task counts.
- Navigates to a web application and performs the necessary interactions to assign tasks.
- Updates the JSON file to set the task count to zero after assignment.
- Maintains logs of task assignments, including dates and details.

## Features

- **Automated Web Interaction**: Utilizes Selenium WebDriver to interact with web elements, including input fields, buttons, and checkboxes.
- **Dynamic Task Processing**: Processes tasks dynamically based on task counts specified in a JSON file.
- **Configurable Start Point**: Allows starting the task assignment from a specified email ID.
- **Error Handling and Logging**: Includes robust error handling and logging to track the execution flow and debug issues effectively.
- **JSON Data Management**: Reads task data from a JSON file and updates the task count after processing each task.

## Requirements

- Python 3.6+
- Selenium
- ChromeDriver

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Rds2151/Toloka-Bot.git
    cd Toloka-Bot
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Download ChromeDriver**:
    Download the appropriate version of ChromeDriver for your Chrome browser from [here](https://developer.chrome.com/docs/chromedriver/downloads), and place it in the `chromedriver` directory.


4. **Create a `.env` File**:
    Create a `.env` file in the root directory with the following content:
    ```
    username = "yt@in.com"
    password = ""
    project_link = ""
    ids_paths="user_ids.json"
    chrome_driver="/home/TokolaBOT/chromedriver-linux64/chromedriver"
    ```

## Usage

1. **Update the JSON File**:
    Modify `task_data.json` to include the email IDs and their corresponding task counts. The script will read from this file and update it after processing.

    ```json
    {
        "dd@in.com": "10",
        "rc@in.com": "20",
        "m@in.com": "30",
        "navi@in.com": "0",
        "lr@in.com": "0",
        "nc@in.com": "0",
        "hb@in.com": "0",
        "a@in.com": "0"
    }
    ```

2. **Run the Script**:
    Execute the script with Python:

    ```bash
    python automate_tasks.py
    ```

3. **Monitor Execution**:
    Check the console output and `selenium_script.log` for detailed logging of the script's execution.

## Configuration

- **Starting Email**:
    Set the `starting_email` variable in the script to the email ID from which you want to begin processing tasks.

    ```python
    starting_email = "m@in.com"
    ```

- **ChromeDriver Path**:
    Ensure the `chrome_driver_path` variable points to the correct location of your ChromeDriver executable.

    ```python
    chrome_driver_path = "/path/to/chromedriver"
    ```

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests to improve the functionality and robustness of the script.

## License

This project is licensed under the MIT License.