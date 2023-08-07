import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import pdfkit
import os
import threading

class Tab2PdfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tab2Pdf")

        # Load the icon file
        icon_path = "icon.ico"  # Replace with the actual icon file name
        self.root.iconbitmap(default=icon_path)

        # Set the window size (width x height)
        self.root.geometry("800x600")  # Adjust the dimensions as needed

        # Create and place the GUI elements
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Starting HTML File", command=self.open_starting_html_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about_dialog)
        self.help_menu.add_command(label="FAQ", command=self.show_faq_dialog)

        # Create a larger font for buttons and labels
        self.larger_font = ('Helvetica', 12)  # Adjust the font size as needed

        self.save_path_label = tk.Label(self.root, text="Save Location:", font=self.larger_font)
        self.save_path_label.pack()

        self.save_path_var = tk.StringVar()
        # Increase the width of the text entry box
        self.save_path_entry = tk.Entry(self.root, textvariable=self.save_path_var, font=self.larger_font, width=40)
        self.save_path_entry.pack()

        self.browse_button = tk.Button(self.root, text="Browse", font=self.larger_font,
                                       command=lambda: self.save_path_var.set(filedialog.askdirectory()))
        self.browse_button.pack()

        # Create a variable to store the browser choice
        self.browser_var = tk.StringVar()
        self.browser_var.set("Firefox")  # Default choice

        # Create a label and option menu for browser choice
        self.browser_label = tk.Label(self.root, text="Select Browser:", font=self.larger_font)
        self.browser_label.pack()

        self.browser_option_menu = tk.OptionMenu(self.root, self.browser_var, "Firefox", "Chrome")
        self.browser_option_menu.pack()

        self.start_button_text = tk.StringVar()
        self.start_button_text.set("Start")
        self.start_button = tk.Button(self.root, textvariable=self.start_button_text, font=self.larger_font, command=self.start_process)
        self.start_button.pack()

        # Create a listbox to display open tabs
        self.open_tabs_listbox = tk.Listbox(self.root, font=self.larger_font, selectmode=tk.MULTIPLE)
        self.open_tabs_listbox.pack(fill=tk.BOTH, expand=True)

    def open_starting_html_file(self):
        html_file_path = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if html_file_path:
            # Load the new HTML file in the initial tab
            self.driver.get('file://' + html_file_path)

    def show_about_dialog(self):
        about_text = "Save PDFs from Tabs\n\nVersion: 0.4\n\nDeveloped by: Amit Nandi"
        messagebox.showinfo("About", about_text)

    # Function to update the open tabs listbox


    def show_faq_dialog(self):
        faq_text = (
            "Frequently Asked Questions\n\n"
            "Q: How do I change the starting HTML file?\n"
            "A: You can change the starting HTML file by selecting 'Open Starting HTML File' from the File menu.\n\n"
            "Q: How can I specify the save location for PDFs?\n"
            "A: You can enter the desired save location in the 'Save Location' text box.\n\n"
            "Q: How does the program work?\n"
            "A: The program opens a Firefox browser, loads tabs from the starting HTML file, and saves PDFs of the tabs.\n\n"
            "Q: Can I customize the PDF save filenames?\n"
            "A: The program automatically names the PDFs as SS1.pdf, SS2.pdf, and so on.\n\n"
            "Q: How do I start the process?\n"
            "A: Click the 'Start' button to begin opening tabs and saving PDFs.\n"
        )
        messagebox.showinfo("FAQ", faq_text)

    def run_browser_and_save_pdfs(self, save_path, browser_choice):


        if browser_choice == "Firefox":
            # Specify the path to the GeckoDriver executable
            gecko_path = r'geckodriver.exe'
            service = FirefoxService(gecko_path)
            self.driver = webdriver.Firefox(service=service)
        elif browser_choice == "Chrome":
            # Specify the path to the ChromeDriver executable
            chrome_path = r'chromedriver.exe'
            service = ChromeService(chrome_path)
            self.driver = webdriver.Chrome(service=service)

        update_thread = threading.Thread(target=self.update_open_tabs_listbox)
        update_thread.daemon = True
        update_thread.start()

        # Load a local HTML file in the initial tab
        html_file_path = r'\starter.html'
        self.driver.get(os.getcwd() + html_file_path)
        print(os.getcwd())
        # Wait for the initial tab content to load (adjust wait time as needed)
        time.sleep(5)

        try:
            # Get the initial number of tabs
            initial_tabs = len(self.driver.window_handles)

            while True:
                # Get the total number of tabs
                total_tabs = len(self.driver.window_handles)

                # Check for newly opened tabs
                if total_tabs > initial_tabs:
                    # Loop through newly opened tabs
                    for tab_index in range(initial_tabs, total_tabs):
                        # Switch to the new tab
                        self.driver.switch_to.window(self.driver.window_handles[tab_index])

                        # Save a screenshot of the current tab content
                        pdf_filename = f'SS{tab_index}.pdf'
                        pdf_path = os.path.join(save_path, pdf_filename)
                        self.save_tab_as_pdf(tab_index, pdf_path)
                        print(f'Saved PDF for tab {tab_index + 1}: {pdf_path}')

                    initial_tabs = total_tabs  # Update the initial tabs count

                    # Show a completion dialog
                    messagebox.showinfo("PDFs Saved", "All PDFs have been saved.")

                time.sleep(5)  # Wait before checking for new tabs again
        except KeyboardInterrupt:
            pass  # Press Ctrl+C to exit the loop

        # Close the WebDriver instance
        self.driver.quit()

    def save_tab_as_pdf(self, tab_index, pdf_path):
        self.driver.switch_to.window(self.driver.window_handles[tab_index])
        try:
            # Create a PDF from the current page using pdfkit
            pdfkit.from_url(self.driver.current_url, pdf_path)
            print(f'Saved PDF for tab {tab_index + 1}: {pdf_path}')
        except Exception as e:
            print(f'Error saving PDF for tab {tab_index + 1}: {e}')


    def update_open_tabs_listbox(self):
        while True:
            open_tabs = self.driver.window_handles
            self.open_tabs_listbox.delete(0, tk.END)
            for tab_index, tab_handle in enumerate(open_tabs):
                tab_title = self.driver.title
                self.open_tabs_listbox.insert(tk.END, f"Tab {tab_index + 1}: {tab_title}")
            time.sleep(2)  # Update every 2 seconds

    def start_process(self):
        save_path = self.save_path_var.get()
        if not save_path:
            save_path = os.getcwd()

        browser_choice = self.browser_var.get()
        driver_thread = threading.Thread(target=self.run_browser_and_save_pdfs, args=(save_path, browser_choice))
        driver_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = Tab2PdfApp(root)
    root.mainloop()
