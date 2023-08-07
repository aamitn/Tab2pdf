# Tab2PDF

Tab2PDF is a Python application that provides a user-friendly way to save newly opened tabs from web browsers (Firefox and Chrome) as PDF files. It streamlines the process of converting web content into PDF documents, making it convenient for users engaged in online research and documentation.

## Features

- Easily switch between Firefox and Chrome browsers.
- Automatically detect and save newly opened tabs as PDF files.
- User-defined save location for PDF files.
- Option to open a starting HTML file and navigate to desired tabs.
- Frequently Asked Questions (FAQ) section for quick reference.
- Real-time display of open tabs with a graphical user interface.

## How to Use

1. Install Python 3.x on your system.
2. Clone this repository or download the source code.
3. Install the required dependencies using the provided `requirements.txt` file:
4. Run the program:
5. Choose your preferred web browser (Firefox or Chrome).
6. Browse and open tabs in your chosen browser.
7. Click the "Start" button in the GUI to save newly opened tabs as PDF files.
8. Specify the save location for the PDF files and click the "Browse" button to choose a directory.
9. Optionally, open a starting HTML file from the "File" menu to navigate to specific tabs.
10. For more information and answers to common questions, refer to the "FAQ" section in the GUI's "Help" menu.

## Commands to Run 
- `pip install -t rquirements.txt`
- `pyinstaller --onefile --noconsole --icon=C:\Users\amit\PycharmProjects\Tab2pdf\dist\icon.ico main.py`
- `pyinstaller main.spec`
Now Run
- `python main.py ` OR -
- `cd dist, main.exe `

## Dependencies

Tab2PDF requires the following Python libraries:

- `tkinter`
- `selenium`
- `pdfkit`

These dependencies can be installed using the provided `requirements.txt` file.

## Compatibility

Tab2PDF has been tested on Windows and may work on other platforms with proper configuration.

## Contributions

Contributions to this project are welcome. Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
