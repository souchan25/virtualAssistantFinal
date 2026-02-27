
import sys
from playwright.sync_api import sync_playwright

def verify_accessibility(page):
    # Navigate to Login
    page.goto('http://localhost:5173/login')
    page.wait_for_load_state('networkidle')

    # Check Login Password Toggle
    # Use a more generic selector to find the button inside the password container
    # The structure is: div.relative > input[type="password"] + button
    toggle_btn_container = page.locator('div.relative:has(input[id="password"])')
    toggle_btn = toggle_btn_container.locator('button')

    if not toggle_btn.is_visible():
        print("Login password toggle button not visible")
        return False

    aria_label = toggle_btn.get_attribute('aria-label')
    print(f"Login Toggle Aria-Label: {aria_label}")

    if aria_label != "Show password":
        print("FAIL: Login toggle initial aria-label incorrect")
        return False

    toggle_btn.click()

    # Wait for Vue to update the DOM if necessary, though aria-label is bound reactively
    # Re-querying or just checking attribute again usually works
    # But since input type changes, the previous selector input[type="password"] might fail if used directly.
    # Here we used a container-based selector which is stable.

    aria_label_after = toggle_btn.get_attribute('aria-label')
    print(f"Login Toggle Aria-Label after click: {aria_label_after}")

    if aria_label_after != "Hide password":
        print("FAIL: Login toggle clicked aria-label incorrect")
        return False

    # Check Forgot Password Modal Close Button
    page.get_by_text("Forgot your password?").click()
    page.wait_for_selector('h3:has-text("Reset Password")')

    close_btn = page.locator('button[aria-label="Close modal"]')
    if not close_btn.is_visible():
         # Fallback to finding by icon if aria-label is missing (which would be a failure)
         print("Forgot password close button with aria-label not found")
         return False
    print("PASS: Forgot password close button has correct aria-label")
    close_btn.click()


    # Navigate to Register
    page.goto('http://localhost:5173/register')
    page.wait_for_load_state('networkidle')

    # Check Register Password Toggle
    reg_pass_container = page.locator('div.relative:has(input[id="password"])')
    reg_pass_toggle = reg_pass_container.locator('button')

    if not reg_pass_toggle.is_visible():
         print("Register password toggle not visible")
         return False

    reg_aria = reg_pass_toggle.get_attribute('aria-label')
    print(f"Register Password Toggle Aria: {reg_aria}")
    if reg_aria != "Show password":
        return False

    # Check Confirm Password Toggle
    confirm_container = page.locator('div.relative:has(input[id="confirm-password"])')
    confirm_toggle = confirm_container.locator('button')

    if not confirm_toggle.is_visible():
        print("Confirm password toggle not visible")
        return False

    confirm_aria = confirm_toggle.get_attribute('aria-label')
    print(f"Confirm Password Toggle Aria: {confirm_aria}")
    if confirm_aria != "Show password":
        return False

    print("ALL ACCESSIBILITY CHECKS PASSED")
    return True

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            if verify_accessibility(page):
                page.screenshot(path='verification_success.png')
                print("Screenshot saved to verification_success.png")
            else:
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()
