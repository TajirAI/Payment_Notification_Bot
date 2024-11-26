import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

def run_browser():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-data-dir=C:\\Users\\Qasim Hameed\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("--profile-directory=Profile 19")

    print("Initializing Chrome Driver!")
    driver = uc.Chrome(options=options)
    driver.maximize_window()

    try:
        # Step 1: Open Gmail in the first tab
        driver.get("https://mail.google.com/mail/u/0/?ogbl#inbox")
        print("Waiting for Gmail to load...")
        time.sleep(5)

        # Step 2: Open WhatsApp Web in a new tab
        # Open a new tab and navigate to WhatsApp Web
        driver.switch_to.new_window('tab')
        driver.get('https://web.whatsapp.com')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[0])  # Switch back to Gmail tab
        print("Gmail and WhatsApp tabs are ready.")

        while True:
            try:
                # Find all unread emails from Meezan Bank Alert
                unread_emails = driver.find_elements(By.XPATH, "//tr[contains(@class, 'zA') and contains(@class, 'zE')]//span[@name='Meezan Bank Alert']")
                if unread_emails:
                    print(f"Found {len(unread_emails)} unread email(s).")

                    for email in unread_emails:
                        try:
                            email.click()
                            time.sleep(1)  # Wait for email content to load

                            # Extract email message content
                            try:
                                message = driver.find_element(By.XPATH, "//div[@role='main']//td[@valign='top']")
                                message_text = message.text.strip()

                                # If message is not accessible or is empty, skip it and go to the next email
                                if not message_text:
                                    print("Email content is not accessible. Skipping this email...")
                                    driver.get("https://mail.google.com/mail/u/0/?ogbl#inbox")  # Go back to inbox
                                    # time.sleep(5)  # Wait for inbox to reload
                                    continue

                                print(f"Extracted Message: {message_text}")

                                # Split the email content into a list of lines
                                message_lines = message_text.split("\n")

                            except NoSuchElementException:
                                print("Email content could not be extracted. Skipping this email...")
                                driver.get("https://mail.google.com/mail/u/0/?ogbl#inbox")  # Go back to inbox
                                # time.sleep(5)  # Wait for inbox to reload
                                continue

                            # Step 3: Switch to WhatsApp tab and send the message
                            driver.switch_to.window(driver.window_handles[1])  # Switch to WhatsApp tab
                            print("Switched to WhatsApp tab.")
                            time.sleep(1)

                            try:
                                # Find a pinned chat and send the message
                                pinned_chat = driver.find_element(By.XPATH, "//span[@data-icon='pinned2']")
                                pinned_chat.click()
                                # time.sleep(2)

                                # Find the message input box
                                message_box = driver.find_element(By.XPATH, "//div[@aria-placeholder='Type a message']")
                                message_box.click()

                                # Send the message as a formatted list
                                for line in message_lines:
                                    message_box.send_keys(line)
                                    message_box.send_keys(Keys.SHIFT, Keys.ENTER)  # Add a new line within the message
                                message_box.send_keys(Keys.ENTER)  # Send the complete message
                                time.sleep(2)
                                print("Message sent successfully!")
                            except NoSuchElementException as e:
                                print(f"Could not find the pinned chat or message box: {str(e)}")
                                continue

                            # Step 4: Switch back to Gmail
                            driver.switch_to.window(driver.window_handles[0])  # Switch back to Gmail tab
                            # time.sleep(2)
                            driver.get("https://mail.google.com/mail/u/0/?ogbl#inbox")
                            # time.sleep(5)  # Wait for Gmail to reload
                        except Exception as e:
                            print(f"Error processing an email: {str(e)}")
                            continue
                else:
                    print("No unread emails found. Checking again in 2 seconds...")

                # Wait before checking again
                time.sleep(2)

            except NoSuchElementException as e:
                print(f"Could not find unread emails: {str(e)}")
                break

    except (WebDriverException, NoSuchElementException) as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
                print("Driver quit successfully.")
            except WebDriverException as e:
                print(f"Error during driver quit: {str(e)}")

run_browser()
