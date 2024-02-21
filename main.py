import xml.etree.ElementTree as ET
from tqdm import tqdm
import pandas as pd
import requests, io, re
from pypdf import PdfReader
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_dataframe(xml_file, crypto=False, vendors=False, initial_data=None):
    is_last_entry = False
    last_entry = None
    if initial_data:
        with open(initial_data, 'rb') as f:
            csv_data = f.read()
        initial_data = pd.read_csv(io.BytesIO(csv_data), sep='\t')
        last_entry = initial_data['Firm CRD Number'].iloc[-1]
    data = {
        'Firm CRD Number': [],
        'Business Name': [],
        'Total Employees': [],
        'AUM': [],
        'Main Website': [],
        # 'Crypto Mentions': [],
        'Vendor Mentions': [],
        'Legal Name': [],
        'Address 1': [],
        'Address 2': [],
        'City': [],
        'State': [],
        'Country': [],
        'Postal Code': [],
        'Phone Number': [],
        'Fax Number': [],
        'Status': [],
        'Date': []
    }
    try:
        # XML data (replace this with your actual XML data)
        with open(xml_file, 'rb') as f:
            xml_data = f.read()


        # Parse the XML data
        root = ET.fromstring(xml_data)

        # Extract data from XML elements
        for firm in tqdm(root.findall('.//Firm')):
            if initial_data is not None:
                if not is_last_entry:
                    if firm.find('Info').attrib.get('FirmCrdNb') != str(last_entry):
                        continue
                    else:
                        is_last_entry = True
                        continue
            firm_info = firm.find('Info')
            main_addr = firm.find('MainAddr')
            rgstn = firm.find('Rgstn')
            item5a = firm.find('.//Item5A')
            item5f = firm.find('.//Item5F')
            item1 = firm.find('.//Item1')
            if item5a.attrib.get('TtlEmp') is None:
                continue
            if int(item5a.attrib.get('TtlEmp')) < 5:
                continue
            mainWebsite = ''
            if item1 is not None:
                web_addrs = item1.find('WebAddrs')
                if web_addrs is not None:
                    web_addr_elements = web_addrs.findall('WebAddr')
                    for web_addr_element in web_addr_elements:
                        url = web_addr_element.text.lower()
                        if ('twitter.com' not in url and 'facebook.com' not in url and 'linkedin.com' not in url and
                                'instagram.com' not in url and 'youtube.com' not in url and 'google.com' not in url
                                and 'vimeo.com' not in url):
                            mainWebsite = url
                            break  # Only consider the first valid website URL
                else:
                    continue

            if crypto:
                mentions = get_brochure_info(firm_info.attrib.get('FirmCrdNb'))
                if mentions < 1:
                    continue
                data['Crypto Mentions'].append(mentions)

            if vendors:
                competitor = get_competitor_mentions_information(firm_info.attrib.get('FirmCrdNb'))
                if not competitor:
                    continue
                data['Vendor Mentions'].append(competitor)

            data['Main Website'].append(mainWebsite)
            data['Firm CRD Number'].append(firm_info.attrib.get('FirmCrdNb'))
            data['Total Employees'].append(item5a.attrib.get('TtlEmp'))
            data['AUM'].append(item5f.attrib.get('Q5F2C'))
            data['Business Name'].append(firm_info.attrib.get('BusNm'))
            data['Legal Name'].append(firm_info.attrib.get('LegalNm'))
            data['Address 1'].append(main_addr.attrib.get('Strt1'))
            data['Address 2'].append(main_addr.attrib.get('Strt2'))
            data['City'].append(main_addr.attrib.get('City'))
            data['State'].append(main_addr.attrib.get('State'))
            data['Country'].append(main_addr.attrib.get('Cntry'))
            data['Postal Code'].append(main_addr.attrib.get('PostlCd'))
            data['Phone Number'].append(main_addr.attrib.get('PhNb'))
            data['Fax Number'].append(main_addr.attrib.get('FaxNb'))
            data['Status'].append(rgstn.attrib.get('St'))
            data['Date'].append(rgstn.attrib.get('Dt'))


        # Create DataFrame
        df = pd.DataFrame(data)
        if initial_data is not False:
            df = pd.concat([initial_data, df], ignore_index=True)

        df.to_csv("RIA_Brochure_Vendor_Mentions.csv", sep='\t', encoding='utf-8')

    except KeyboardInterrupt:
        df = pd.DataFrame(data)
        if initial_data is not False:
            df = pd.concat([initial_data, df], ignore_index=True)

        df.to_csv("RIA_Brochure_Vendor_Mentions_Incomplete.csv", sep='\t', encoding='utf-8')

    except ConnectionError:
        df = pd.DataFrame(data)

        df.to_csv("RIA_Brochure_Vendor_Mentions_Incomplete.csv", sep='\t', encoding='utf-8')


def get_competitor_mentions_information(crd_num):
    def visitor(content, cm, tm, font_dict, font_size):
        y = cm[5]
        if 0 < y < 1008:
            raw_text.append(content)
    base_url = 'https://reports.adviserinfo.sec.gov/reports/ADV/'
    url = f'{base_url}{crd_num}/PDF/{crd_num}.pdf'
    r = requests.get(url, stream=True)
    try:
        pdf = PdfReader(io.BytesIO(r.content))
    except Exception as e:
        print(e)
        return None
    get_vendor_name = r"Name of entity where books and records are kept:(.*?)Number and Street 1:"
    get_vendor_description = r"Briefly describe the books and records kept at this location\.(.*?)(?:Name of entity where books and records are kept:|SECTION 1\.)"

    # extract text and do the search
    entries = []
    vendors, vendor_descriptions = [], []
    text = ''
    for page in pdf.pages:
        raw_text = []
        page.extract_text(visitor_text=visitor)
        new_text = ' '.join(raw_text)
        text += new_text
    vendors += re.findall(get_vendor_name, text, re.DOTALL)
    vendor_descriptions += re.findall(get_vendor_description, text, re.DOTALL)
    keywords = [
        'Adviser Compliance Associates', 'Complysci', 'Orion', 'PTCC', 'MyComplianceOffice', 'BasisCode', 'Orion',
        'gVue', 'Compliance Alpha', 'ComplianceAlpha', 'RegEd', 'Protegent', 'ACA ', 'Outsource CCO', 'Aspect',
        'Vigilant']
    for i in range(len(vendors)):
        if any(x.lower() in vendors[i].lower() for x in keywords):
            new_entry = {
                'vendor_name': vendors[i].replace('\n', ''),
                'vendor_description': vendor_descriptions[i].replace('\n', '')
            }
            entries.append(new_entry)
    if len(entries) == 0:
        return None
    print(entries)
    return entries[0]


def get_brochure_info(crd_num):
    base_url = 'https://adviserinfo.sec.gov/firm/summary/'
    display = Display(visible=False, size=(800, 600))
    display.start()
    browser = webdriver.Firefox()
    main_url = f'{base_url}{crd_num}'
    browser.get(main_url)
    delay = 0.5  # seconds
    try:
        print(WebDriverWait(browser, delay).until(EC.presence_of_element_located((
            By.CLASS_NAME, 'btn btn-md btn-accent firmbutton ng-star-inserted'))))
    except TimeoutException:
        pass
    soup = BeautifulSoup(browser.page_source, 'lxml')
    buttons = soup.find_all('a', class_='btn btn-md btn-accent firmbutton ng-star-inserted')
    url = buttons[1]['href']
    if 'http' not in url:
        return 0
    r = requests.get(url, stream=True)
    pdf = PdfReader(io.BytesIO(r.content))
    crypto_mentions = 0
    for page in pdf.pages:
        text = page.extract_text()
        crypto_mentions += text.lower().count('crypto')
    browser.quit()
    print(crypto_mentions)
    return crypto_mentions

if __name__ == '__main__':
    get_dataframe('SEC Scraping/SEC_DataDump.xml', vendors=True, initial_data='SEC Scraping/RIA_Brochure_Vendor_Mentions_Incomplete.csv')
