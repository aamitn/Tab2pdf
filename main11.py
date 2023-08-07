from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time
import pdfkit
import os

# Specify the path to the GeckoDriver executable
gecko_path = r'geckodriver.exe'
service = Service(gecko_path)

# Create a Firefox WebDriver instance
driver = webdriver.Firefox(service=service)

# Load a local HTML file in the initial tab
html_file_path = r'C:\Users\amit\Desktop\ulproj\Unified_Launcher.html'
driver.get('file://' + html_file_path)

# Wait for the initial tab content to load (adjust wait time as needed)
time.sleep(5)

# Function to save the entire page as PDF
def save_tab_as_pdf(tab_index, pdf_path):
    driver.switch_to.window(driver.window_handles[tab_index])

    # Create a PDF from the current page using pdfkit
    pdfkit.from_url(driver.current_url, pdf_path)

# Get the path to save PDFs from the user
pdf_save_path = input('Enter the path to save PDFs (leave blank for root path): ').strip()
if not pdf_save_path:
    pdf_save_path = ''

# Create the specified directory if it doesn't exist
os.makedirs(pdf_save_path, exist_ok=True)

# Add a delay to keep the browser window open
try:
    while True:
        # Get the total number of tabs
        total_tabs = len(driver.window_handles)

        # Loop through newly opened tabs
        for tab_index in range(1, total_tabs):
            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[tab_index])

            # Save the entire page as PDF
            pdf_filename = f'SS{tab_index}.pdf'
            pdf_path = os.path.join(pdf_save_path, pdf_filename)
            save_tab_as_pdf(tab_index, pdf_path)

        time.sleep(5)  # Wait before checking for new tabs again
except KeyboardInterrupt:
    pass  # Press Ctrl+C to exit the loop

# Close the WebDriver instance
driver.quit()