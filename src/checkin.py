import time
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

def main():
    print("Starting the Hoyoverse Daily Check-In Bot...")
    load_dotenv()
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)  # headless=False shows the browser
            page = browser.new_page()
            page.goto("https://www.hoyolab.com/home")
        except Exception as e:
            print(f"Failed to launch browser or navigate to homepage: {e}")
            time.sleep(600)  # 10 minutes for debugging
            return

        try:
            iframe_element = page.wait_for_selector("iframe[id='hyv-account-frame']", state="visible")
            login_frame = iframe_element.content_frame()
        except Exception as e:
            print(f"Failed to find or access login iframe: {e}")
            time.sleep(600)  # 10 minutes for debugging
            browser.close()
            return

        try:
            # Wait for the username and password fields to be visible
            login_frame.wait_for_selector("input[name='username']", state="visible")
            login_frame.wait_for_selector("input[name='password']", state="visible")
            print("HYV_EMAIL:", os.getenv("HYV_EMAIL"))
            print("HYV_PASSWORD:", "*" * len(os.getenv("HYV_PASSWORD")))
            # Fill in the username and password fields
            login_frame.type("input[name='username']", os.getenv("HYV_EMAIL"), delay=25)
            login_frame.type("input[name='password']", os.getenv("HYV_PASSWORD"), delay=25)
            login_button = login_frame.locator("button", has_text="Log In")
            login_button.wait_for(state="visible")
            with page.expect_popup() as popup_info:
                login_button.click()
            
            auth_popup = popup_info.value
            print(f"Popup opened: Authentication in process...")
            
            # Wait for the popup to close (this will block until it closes)
            auth_popup.wait_for_event("close")
            print("Popup closed - Authentication completed!")

            page.wait_for_load_state("domcontentloaded")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Failed to login: {e}")
            time.sleep(600)  # 10 minutes for debugging
            browser.close()
            return

        try:
            # Skip recommendations modal
            skip_button = page.locator("button", has_text="Skip")
            skip_button.wait_for(state="visible")
            skip_button.click()
        except Exception as e:
            print(f"Failed to skip recommendations modal: {e}")
            time.sleep(600)
            browser.close()
            return

        try:
            # Load interest group page
            interest_group_button = page.locator("div[class='topbar-game-select']", has_text="Interest Group")
            interest_group_button.wait_for(state="visible")
            interest_group_button.click()
        except Exception as e:
            print(f"Failed to click Interest Group button: {e}")
            time.sleep(600)
            browser.close()
            return

        try:
            # Click on Genshin Impact button
            genshin_impact_button = page.locator("div[class='game-name']", has_text="Genshin Impact")
            genshin_impact_button.wait_for(state="visible")
            genshin_impact_button.click()
        except Exception as e:
            print(f"Failed to click Genshin Impact button: {e}")
            time.sleep(600)
            browser.close()
            return

        try:
            # Click on Check-In button
            checkin_button = page.locator("div[class='tool-name']").get_by_text("Check-In", exact=True)
            checkin_button.wait_for(state="visible")

            # Handle the popup that opens when clicking the Check-In button
            with page.expect_popup() as popup_info:
                checkin_button.click()
            genshin_checkin_page = popup_info.value
            print("Successfully opened Genshin Check-In!")
        except Exception as e:
            print(f"Failed to open Genshin Check-In page: {e}")
            time.sleep(600)  # 10 minutes for debugging
            browser.close()
            return

        try:
            # Wait for the popup page to load completely
            genshin_checkin_page.wait_for_load_state("domcontentloaded")
            genshin_checkin_page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Failed to wait for popup page to load: {e}")
            print(f"Popup page URL: {genshin_checkin_page.url if 'genshin_checkin_page' in locals() else 'Not available'}")
            time.sleep(600)  # 10 minutes for debugging
            browser.close()
            return

        try:
            # Close the modal that appears on the check-in page
            close_button = genshin_checkin_page.locator("span[class*='guide-close']")
            close_button.wait_for(state="visible")
            close_button.click()
        except Exception as e:
            print(f"Failed to close modal on check-in page: {e}")
            time.sleep(600)
            browser.close()
            return

        try:
            # Look for the day count element
            day_span = genshin_checkin_page.locator("span[class='sign-num']")
            day_span.wait_for(state="visible")
            day_count = int(day_span.text_content()) + 1

            print(f"Looking for Day {day_count} rewards...")
        except Exception as e:
            print(f"Failed to get Genshin day count: {e}")
            time.sleep(600)
            browser.close()
            return

        try:
            # Click on the reward button for the current day
            reward_button = genshin_checkin_page.locator("div[class*='item-day']").get_by_text(f"Day {day_count}", exact=True)
            reward_button.wait_for(state="visible")
            reward_button.click()
            rewards_close_button = genshin_checkin_page.locator("div[class*='dialog-close']")
            rewards_close_button.wait_for(state="visible")
            rewards_close_button.click()
            print("Genshin rewards successfully claimed!")
        except Exception as e:
            print(f"Failed to click reward button for day {day_count}: {e}")
            pass
        # Close Genshin Check-In page, navigate to HSR page
        try:
            genshin_checkin_page.close()
            hsr_button = page.locator("div[class='game-name']:not(#header div[class='game-name'])").get_by_text("Honkai: Star Rail", exact=True)
            hsr_button.wait_for(state='visible')
            with page.expect_navigation():
                hsr_button.click()
        except Exception as e:
            print(f"Failed to close Genshin Check-In and navigate to HSR Page: {e}")
            time.sleep(600)
            browser.close()
            return
        # Load HSR page
        try:
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Failed to open HSR page {e}")
            time.sleep(600)
            browser.close()
            return
        
        # Navigate to HSR Check-In page
        try:
            hsr_checkin_button = page.locator("div[class='tool-name']").get_by_text("Check In", exact=True)
            hsr_checkin_button.wait_for(state="visible")
            with page.expect_popup() as popup_info:
                hsr_checkin_button.click()
            hsr_checkin_page = popup_info.value
        except Exception as e:
            print(f"Failed to open HSR Check-In Page: {e}")
            time.sleep(600)
            browser.close()
            return
        # Wait for DOM to be loaded and network to be idle on HSR Check-In Page
        try:
            hsr_checkin_page.wait_for_load_state("domcontentloaded")
            hsr_checkin_page.wait_for_load_state("networkidle")
            print("Successfully opened HSR Check-In!")
        except Exception as e:
            print(f"Failed to wait for HSR Check-In Page to load: {e}")
            time.sleep(600)
            browser.close()
            return
        # Wait for notification pop-up to appear and close
        try:
            notifications_close_button = hsr_checkin_page.locator("div[class*='dialog-close']")
            notifications_close_button.wait_for(state="visible")
            notifications_close_button.click()
        except Exception as e:
            print(f"Failed to close the HSR notifications pop-up.")
            pass
        # Locate Day Count for HSR Check-In
        try:
            paragraph = hsr_checkin_page.locator("p", has_text="Checked in for")
            span_element = paragraph.locator("span[style*='rgba(255, 170, 42, 1)']")
            day_count = int(span_element.text_content()) + 1
            print(f"Looking for HSR Day {day_count} rewards...")
        except Exception as e:
            print(f"Failed to get HSR day count: {e}")
            time.sleep(600)
            browser.close()
            return
        
        try:
            reward_button = hsr_checkin_page.locator("span").get_by_text(f"Day {day_count}", exact=True)
            reward_button.wait_for(state="visible")
            reward_button.click()
            rewards_close_button = hsr_checkin_page.locator("div[class*='dialog-close']")
            rewards_close_button.wait_for(state="visible")
            rewards_close_button.click()
            print("Honkai: Star Rail rewards successfully claimed!")
        except Exception as e:
            print(f"Failed to claim HSR rewards: {e}")
            pass

        # Close HSR Check-In page and open ZZZ page
        try:
            hsr_checkin_page.close()
            zzz_button = page.locator("div[class='game-name']:not(#header div[class='game-name'])").get_by_text("Zenless Zone Zero", exact=True)
            zzz_button.wait_for(state='visible')
            with page.expect_navigation():
                zzz_button.click()
        except Exception as e:
            print(f"Failed to close HSR and navigate to ZZZ Page: {e}")
            time.sleep(600)
            browser.close()
            return
        
        # Open ZZZ Check-In page
        try:
            zzz_checkin_button = page.locator("div[class='tool-name']").get_by_text("Check In", exact=True)
            zzz_checkin_button.wait_for(state='visible')
            with page.expect_popup() as popup_info:
                zzz_checkin_button.click()
            zzz_checkin_page = popup_info.value
        except Exception as e:
            print(f"Failed to open ZZZ Check-In page: {e}")
            time.sleep(600)
            browser.close()
            return
        
        # Wait for ZZZ Check In page to load
        try:
            zzz_checkin_page.wait_for_load_state("domcontentloaded")
            zzz_checkin_page.wait_for_load_state("networkidle")
            print("Successfully opened ZZZ Check-In!")
        except Exception as e:
            print(f"Failed to load ZZZ Check-In page: {e}")
            time.sleep(600)
            browser.close()
            return
        
        # Close ZZZ notifications popup
        try:
            notifications_close_button = zzz_checkin_page.locator("div[class*='dialog-close']")
            notifications_close_button.wait_for(state='visible')
            notifications_close_button.click()
        except Exception as e:
            print(f"Failed to close ZZZ popup: {e}")
            pass
        
        # Get ZZZ day count
        try:
            paragraph = zzz_checkin_page.locator("p", has_text="Checked in for")
            day_text = paragraph.locator("span[style*='color:rgba(250, 124, 22, 1)']")
            day_text.wait_for(state="visible")
            day_count = int(day_text.text_content()) + 1
        except Exception as e:
            print(f"Failed to get ZZZ day count: {e}")
            time.sleep(600)
            browser.close()
            return

        # Claim ZZZ rewards
        try:
            rewards_button = zzz_checkin_page.locator("div[class*='item']").get_by_text(f"Day {day_count}", exact=True)
            rewards_button.wait_for(state="visible")
            rewards_button.click()
            rewards_close_button = zzz_checkin_page.locator("div[class*='dialog-close']")
            rewards_close_button.wait_for(state="visible")
            rewards_close_button.click()
            print("Zenless Zone Zero rewards successfully claimed!")
        except Exception as e:
            print(f"Failed to claim ZZZ rewards: {e}")
            pass
    
        time.sleep(5)
        print("Ending the program...")
        browser.close()
        return
    
if __name__ == "__main__":
    main()
