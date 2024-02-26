# Project Name

## Overview
This project contains a collection of Python scripts designed to scrape data from PDF files hosted on the U.S. Securities and Exchange Commission (SEC) website. The scripts aim to extract information about companies that either use specific software solutions or are involved in dealing with cryptocurrencies. The extracted data can provide insights into the adoption of certain technologies or the prevalence of cryptocurrency-related activities among publicly traded companies.

## Features
- **PDF Scraping**: Utilizes `pypdf` to extract text and data from PDF documents.
- **Keyword Search**: Searches for specific keywords related to software usage or cryptocurrency activities within the extracted text.
- **Data Output**: Provides structured data output, such as CSV files or database entries, for further analysis.
- **Customizable**: Easily customizable to adapt to different search criteria or PDF formats.

## Scripts
1. `main.py`: Scrapes PDF documents to identify companies that mention specific software solutions.
2. `cryptor.py`: Extracts information about companies involved in cryptocurrency-related activities from PDF files.

## Usage
1. Clone the repository to your local machine:

```bash
git clone https://github.com/otisscott/sec_scraping.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the desired script, providing necessary arguments such as keywords or file paths:

```bash
python main.py
```

## Requirements
- Python 3.x
- Dependencies listed in `requirements.txt`
- Access to the internet to download PDF files from the SEC website.
- A locally saved copy of the XML file containing all of the registered investment advisers found here: https://adviserinfo.sec.gov/compilation

## Contribution
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Disclaimer
This project is intended for educational and research purposes only. The information extracted from SEC filings should be verified and used responsibly. The creators of this project are not responsible for any misuse of the data obtained through these scripts.

## License
[MIT License](LICENSE)
