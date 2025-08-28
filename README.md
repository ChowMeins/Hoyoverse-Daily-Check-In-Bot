# HoyoVerse Game Daily Rewards Claimer (Playwright + Docker)

This is the updated version of the project that automates claiming daily rewards for 
**Genshin Impact**, **Honkai: Star Rail**, and **Zenless Zone Zero** using **Playwright** 
and **Docker**.  

> ⚠️ A Selenium version is available on the `selenium-legacy` branch.

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.10 or higher**  
- **Playwright** and **Python dotenv**  
  Install dependencies while in the root directory:
  ```sh
  pip install -r requirements.txt

## Configuration

This project requires a .env file to log in to the HoyoLab website.

In the project's root directory, create a file named .env.

Add the following content, replacing the placeholders with your actual credentials:

**`.env` file**
```
HYV_EMAIL="your_email@example.com"
HYV_PASSWORD="your_password"
```

## Execution

Running the Python Script Directly

Once setup, run the Python script while in the src folder:

`python checkin.py`

Running with Docker (Optional)

Build and start the container:

`docker compose up --build`


The script will execute inside the container automatically.
