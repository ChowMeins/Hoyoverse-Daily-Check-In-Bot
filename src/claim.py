from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import logging
import datetime

def loadEnvVariables() -> list[str]:
    load_dotenv()
    return [os.getenv("HYV_EMAIL"), os.getenv("HYV_PASSWORD")]

def removeEnvVariables():
    os.environ.pop("HYV_EMAIL", None)  # Removes if exists, otherwise does nothing
    os.environ.pop("HYV_PASSWORD", None)

def save_page_source(driver, error_name="error"):
    """Save the current page's HTML source with a timestamped filename."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{error_name}_{timestamp}.html"  # Unique filename

    with open(filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    logging.debug(f"Saved page source to {filename}")  # Log the saved file

def main():
    logging.basicConfig(
        filename="hyv_errors.log",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    service = Service(executable_path='chromedriver')
    driver = webdriver.Chrome(service=service)
    userCredentials = loadEnvVariables()

    # Load into HoyoLab official website
    hoyolab_website = 'https://www.hoyolab.com/home'
    driver.get(hoyolab_website)
    actions = ActionChains(driver)
    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'hyv-account-frame')))
        loginFrame = driver.find_element(By.ID, 'hyv-account-frame')
        driver.switch_to.frame(loginFrame)
    except:
        logging.error("Can't find login frame.")
        save_page_source(driver)
    # Switch to the iFrame containing the login modal
    print('Hoyoverse Login Frame Found.')

    # Enter user information to login
    try:
        email = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/form/div[3]/div[1]/input')
        email.send_keys(userCredentials[0])
        password = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/form/div[4]/div[1]/input')
        password.send_keys(userCredentials[1])
        loginButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/form/button')
        loginButton.click()
        driver.switch_to.default_content()
    except:
        logging.error("Error trying to login")
        save_page_source(driver)

    try:
    # Skip recommendation tabs
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div/div[1]/button')))
        skipButton = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div/div[1]/button')
        skipButton.click()
    except:
        logging.error("Error trying to skip recommendation pop-up")
        save_page_source(driver)

    try:
    # Click Interest Groups to show list of games
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div[2]/div[1]/p')))
        interestGroupButton = driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div[2]/div[1]/p')
        interestGroupButton.click()
    except:
        logging.error("Error trying find interest group button.")
        save_page_source(driver)

    hoyolab_window = driver.current_window_handle
    
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div[2]/div[1]')))
        interestGroupButton = driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div[2]/div[1]')
        actions.move_to_element(interestGroupButton).perform()
    except:
        logging.error("Error trying to hover over interest group button for GI.")
        save_page_source(driver)
    # Click Genshin Impact
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/a[1]')))
        genshinTab = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/a[1]')
        genshinTab.click()
        time.sleep(5)
    except:
        logging.error("GI: Error trying to find the GI tab under interest groups")
        save_page_source(driver)

    # Click Daily Check-In
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div')))
        genshinCheckIn = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div')
        genshinCheckIn.click()
        time.sleep(3)
    except:
        logging.error("GI: Error trying find the check-in button")
        save_page_source(driver)

    # Switch Driver to Genshin Impact Daily Rewards tab
    try:
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        print("Genshin Daily Check-In Opened!")
    except:
        logging.error("GI: Daily Check-in never opened")
        save_page_source(driver)    

    # Close reminder popup
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/span')))
        closeButton = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/span')
        closeButton.click()
    except:
        logging.error("GI: Error trying to find the number of daily rewards claimed.")
        save_page_source(driver)

    daysClaimed = None
    
    try:
    # Claim daily reward
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[5]/div/div/div/div[1]/div[1]/div[1]/span')))
        dayText = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div/div/div[1]/div[1]/div[1]/span')
        daysClaimed = int(dayText.text) + 1
    except:
        logging.error("GI: Days claimed not found text.")
        save_page_source(driver)
    if daysClaimed != None:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Day {daysClaimed}')]")))
            dailyReward = driver.find_element(By.XPATH, f"//*[contains(text(), 'Day {daysClaimed}')]")
            dailyReward.click()
            time.sleep(5)
        except:
            logging.error(f"GI: Day {daysClaimed} not found. Failed to claim reward.")
            save_page_source(driver)
    # Switch back to Hoyolabs page    
    driver.close()
    driver.switch_to.window(hoyolab_window)
    time.sleep(2)

    # Hover to interest group tab
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]')))
        interestGroupButton.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div[2]')
        actions.move_to_element(interestGroupButton).perform()
    except:
        logging.error("HSR: Error trying to find interest group tab.")
        save_page_source(driver)
    
    # Hover over HSR and click
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/a[2]')))
        hsrTab = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/a[2]')
        actions.move_to_element(hsrTab).click().perform()
        time.sleep(5)
    except:
        logging.error("HSR: Error trying to find HSR under interest group tab.")
        save_page_source(driver)
        
    # Click Daily Check-In
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div')))
        hsrCheckIn = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div')
        hsrCheckIn.click() # Will open the HSR Daily Check-In
        time.sleep(3)
    except:
        logging.error("HSR: Error trying find the check-in button.")
        save_page_source(driver)
    
    try:
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        print("Honkai Star Rail Daily Check-In Opened!")
    except:
        logging.error("HSR: Daily Check-in never opened.")
        save_page_source(driver)    
    
    time.sleep(2)
    # Close reminder popup on daily check-in website
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div')))
        closeButton = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div')
        closeButton.click()
    except:
        logging.error("HSR: Reminder pop-up not found.")
        save_page_source(driver)          

    # Claim rewards
    daysClaimed = None
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div[4]/div/div[1]/div[1]/p[1]/span')))
        dayText = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[4]/div/div[1]/div[1]/p[1]/span')
        daysClaimed = int(dayText.text) + 1
    except:
        logging.error("HSR: Days claimed not found.")
        save_page_source(driver)      
    if daysClaimed != None:
        try:
            dailyReward = driver.find_element(By.XPATH, f"//*[text() = 'Day {daysClaimed}']")
            dailyReward.click()
            time.sleep(5)
        except:
            logging.error("HSR: Rewards not claimed.")
            save_page_source(driver)        

    # Close current tab and switch back to Hoyoverse Lab
    driver.close()
    driver.switch_to.window(hoyolab_window)
    time.sleep(2)

    # Hover over interest group tab
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div[2]/div[1]')))
        interestGroupButton = driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div[2]/div[1]')
        actions.move_to_element(interestGroupButton).perform()
    except:
        logging.error("ZZZ: Error trying to find interest group.")
        save_page_source(driver)

    # Hover over ZZZ tab and click
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/a[3]')))
        zzzTab = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/a[3]')
        actions.move_to_element(zzzTab).click().perform()
        time.sleep(5)
    except:
        logging.error("ZZZ: Error trying to find ZZZ under interest tab.")
        save_page_source(driver)  

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div/div/div[2]/div/div')))
        zzzCheckIn = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div/div/div[2]/div/div')
        zzzCheckIn.click()
    except:
        logging.error("ZZZ: Daily Check-In not found.")
        save_page_source(driver)  

    try:
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        print("ZZZ Daily Check-in Opened!")
        time.sleep(3)
    except:
        logging.error("ZZZ: Daily Check-In never opened.")
        save_page_source(driver)   
    
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div')))
        closeButton = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div')
        closeButton.click()
    except:
        logging.error("ZZZ: Recommendation pop-up not.")
        save_page_source(driver)  

    daysClaimed = None
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div[4]/div/div[1]/div[1]/p[1]/span')))
        dayText = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[4]/div/div[1]/div[1]/p[1]/span')
        daysClaimed = int(dayText.text) + 1
    except:
        logging.error("ZZZ: Days claimed not found.")
        save_page_source(driver)

    if daysClaimed != None:
        try:    
            dailyReward = driver.find_element(By.XPATH, f"//*[text() = 'Day {daysClaimed}']")
            dailyReward.click()
            time.sleep(5)
        except:
            logging.error("ZZZ: Rewards not claimed.")
            save_page_source(driver)
    
    driver.quit()

if __name__ == '__main__':
    removeEnvVariables()
    main()
