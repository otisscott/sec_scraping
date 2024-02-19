import requests, io, re
import pandas as pd
import ast

with open('SEC Scraping/RIA_Brochure_Vendor_Mentions_Incomplete.csv', 'rb') as f:
    csv_data = f.read()

firm_data = pd.read_csv(io.BytesIO(csv_data), sep='\t', header=0)

keywords = [
        'Adviser Compliance Associates', 'ComplySci', 'Orion', 'PTCC', 'MyComplianceOffice', 'BasisCode', 'Orion',
        'gVue', 'Compliance Alpha', 'ComplianceAlpha', 'RegEd', 'Protegent', 'ACA ', 'Outsource CCO', 'Aspect',
        'Vigilant']

data = {
        'Firm CRD Number': [],
        'Business Name': [],
        'Total Employees': [],
        'AUM': [],
        'Main Website': [],
        # 'Crypto Mentions': [],
        'Vendor': [],
        'Vendor Descriptions': [],
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

for index, row in firm_data.iterrows():
    data['Main Website'].append(row['Main Website'])
    data['Firm CRD Number'].append(row['Firm CRD Number'])
    data['Total Employees'].append(row['Total Employees'])
    data['AUM'].append(row['AUM'])
    data['Business Name'].append(row['Business Name'])
    data['Legal Name'].append(row['Legal Name'])
    data['Address 1'].append(row['Address 1'])
    data['Address 2'].append(row['Address 2'])
    data['City'].append(row['City'])
    data['State'].append(row['State'])
    data['Country'].append(row['Country'])
    data['Postal Code'].append(row['Postal Code'])
    data['Phone Number'].append(row['Phone Number'])
    data['Fax Number'].append(row['Fax Number'])
    data['Status'].append(row['Status'])
    data['Date'].append(row['Date'])

    vendor_info = ast.literal_eval(row['Vendor Mentions'])

    for keyword in keywords:
        if keyword.lower() in vendor_info['vendor_name'].lower():
            data['Vendor'].append(keyword)
            data['Vendor Descriptions'].append(vendor_info['vendor_description'])
            print(row['Business Name'],vendor_info)
            break

df = pd.DataFrame(data)

# df.to_csv("RIA_Brochure_Vendor_Mentions_Incomplete_Normalized.csv", sep='\t', encoding='utf-8')