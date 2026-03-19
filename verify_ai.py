from playwright.sync_api import sync_playwright, expect
import os

def test_app():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="/home/jules/verification/video_ai")
        page = context.new_page()

        try:
            page.goto("http://localhost:5173")
            page.wait_for_timeout(1000)

            page.get_by_text("Start Exam Now").click()
            page.wait_for_timeout(1000)

            page.get_by_text("It provides full-duplex service.").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Save & Next").click()
            page.wait_for_timeout(1000)

            # Need to handle dialog BEFORE clicking submit because page.on applies asynchronously but .click() can block if dialog pops up
            page.once("dialog", lambda dialog: dialog.accept())
            page.get_by_role("button", name="Submit Exam").click()
            page.wait_for_timeout(1000)

            page.get_by_text("Generate AI Performance Analysis").click()

            # Wait for AI report to generate (2 seconds simulated)
            page.wait_for_timeout(2500)

            expect(page.get_by_text("Performance Insights")).to_be_visible()

            page.screenshot(path="/home/jules/verification/verification_ai.png")
            page.wait_for_timeout(2000)

        except Exception as e:
            print(f"Error during test: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/video_ai", exist_ok=True)
    test_app()