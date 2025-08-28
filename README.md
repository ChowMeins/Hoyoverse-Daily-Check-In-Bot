# **HoyoVerse Game Daily Rewards Claimer**

> **Disclaimer:** This is the legacy version of the project written using Selenium. 
> For the latest version with Playwright and Docker, please check the `main` branch.

This project automates claiming rewards from daily check-ins for **Genshin Impact**, **Honkai: Star Rail**, and **Zenless Zone Zero**

## Prerequisites

Ensure you have the following installed:

- ## **Python** (developed using Python 3.10.11)
- ## Installation of both the Selenium library and Python dotenv.
    - run the following while in the root directory:
    ```
    pip install -r requirements.txt
    ```
- ## Installation of a chromedriver
    - Go to the following website to install a chromedriver for your system.
    - https://googlechromelabs.github.io/chrome-for-testing/
    - Once installed, place the chromedriver.exe file into the src folder
      - **You may have to change line 39 of the Python file to make the executable path match the file name of the chromedriver installed**
      ```
      service = Service(executable_path='{Insert the chromedriver file name here')
      ```

## Configuration

This project requires a `.env` file to be able to login to the HoyoLab website.  

### Creating the `.env` File  

1. In the project's root directory, create a file named `.env`.
2. Add the following content, replacing the placeholders with your actual credentials:

   ```
   HYV_EMAIL=your_email@example.com
   HYV_PASSWORD=your_password
   ```

## Execution
Once setup, run the Python script while in the src folder.
``` 
python claim.py 
```

