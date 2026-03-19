from playwright.sync_api import sync_playwright, expect
import os

def test_app():
    with sync_playwright() as p:
        # Start browser and recording context
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="/home/jules/verification/video")
        page = context.new_page()

        try:
            # 1. Load application
            page.goto("http://localhost:5173")
            page.wait_for_timeout(1000)

            # 2. Start Exam Now (uses sample test)
            page.get_by_text("Start Exam Now").click()
            page.wait_for_timeout(1000)

            page.get_by_role("checkbox").check()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="I am ready to begin").click()
            page.wait_for_timeout(1000)

            # 3. Answer Question 1 (MCQ) - Correct Answer is 'It provides full-duplex service.'
            page.get_by_text("It provides full-duplex service.").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Save & Next").click()
            page.wait_for_timeout(1000)

            # 4. Answer Question 2 (NAT) - Correct Answer is '48'
            page.get_by_placeholder("0.00").fill("48")
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Mark for Review & Next").click()
            page.wait_for_timeout(1000)

            # 5. Answer Question 3 (MSQ) - Correct Answer is 'Merge Sort', 'Heap Sort'
            page.get_by_text("Merge Sort").click()
            page.get_by_text("Heap Sort").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Save & Next").click()
            page.wait_for_timeout(1000)

            # 6. Verify "Previous" button exists and works
            page.get_by_role("button", name="Previous").click()
            page.wait_for_timeout(500)
            # Should be back to NAT question
            expect(page.get_by_text("Consider the matrix A with")).to_be_visible()

            # 7. Submit exam from sidebar
            page.get_by_role("button", name="Submit Exam").click()
            # Handle confirm dialog
            page.on("dialog", lambda dialog: dialog.accept())
            page.wait_for_timeout(1000)

            # 8. Take Result Screenshot
            page.screenshot(path="/home/jules/verification/verification.png")
            page.wait_for_timeout(2000)

        except Exception as e:
            print(f"Error during test: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/video", exist_ok=True)
    test_app()
