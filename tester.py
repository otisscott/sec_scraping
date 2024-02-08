import requests, io, re
from pypdf import PdfReader


def get_competitor_mentions_information():
    crd_lst = ['109330', '294670']
    base_url = 'https://reports.adviserinfo.sec.gov/reports/ADV/'
    for crd_num in crd_lst:
        url = f'{base_url}{crd_num}/PDF/{crd_num}.pdf'
        r = requests.get(url, stream=True)
        pdf = PdfReader(io.BytesIO(r.content))
        get_vendor_name = r"Name of entity where books and records are kept:(.*?)Number and Street 1:"
        get_vendor_description = r"Briefly describe the books and records kept at this location\.(.*?)(?:Name of entity where books and records are kept:|SECTION 1\.)"

        # extract text and do the search
        entries = []
        vendors, vendor_descriptions = [], []
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        vendors += re.findall(get_vendor_name, text, re.DOTALL)
        vendor_descriptions += re.findall(get_vendor_description, text, re.DOTALL)
        keywords = ['ethics', 'compliance']
        print(vendors, vendor_descriptions)
        for i in range(len(vendors)):
            if any(x in vendor_descriptions[i].lower() for x in keywords):
                new_entry = {
                    'vendor_name': vendors[i],
                    'vendor_description': vendor_descriptions[i]
                }
                entries.append(new_entry)
        print(entries)
