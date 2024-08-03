import base64
import os

import pandas as pd


def decoded_body(body, is_base64_encoded=False):
    if is_base64_encoded and body:
        try:
            return base64.b64decode(body.encode()).decode('latin-1')
        except:
            return base64.b64decode(body.encode()).decode('latin-1', errors='ignore')
    return body



def encode_body(string_body):
    # Convert the input string to bytes
    try:
        byte_data = string_body.encode('utf-8')
        print(f"Encoded string: {string_body}")
    except UnicodeEncodeError:
        print(f"Error ignore encoding string: {string_body}")
        byte_data = string_body.encode('utf-8', errors='ignore')

    # Decode the base64 encoded bytes
    binary_data = base64.b64decode(byte_data)

    return binary_data


def fetch_request_body_file(body, boundary):
    string_decoded_body = body

    parts = string_decoded_body.split(boundary)

    request_body = {
        'filename': None,
        'file_content': None
    }

    for part in parts:

        if 'Content-Disposition' not in part:
            continue

        content_disposition = part.split(f'Content-Disposition:')[1].strip()
        print("Content-Disposition: ", content_disposition[:50])
        print("Part: ", part[:50])

        if request_body.get('filename') is None and "filename" in part:
            extension = '.xlsx' if '.xlsx' in content_disposition else (
                '.XLSX' if '.XLSX' in content_disposition else None)
            request_body['filename'] = content_disposition.split(f'filename=')[1].strip('"').split(extension)[
                                           0] + '.xlsx'
            request_body['file_content'] = part.split("\r\n\r\n")[1].rstrip("\r\n--")
            print("=" * 88)
            print("=====> File Name: ", request_body['filename'])
            print("=" * 88)
            continue

    request_body = {
        'filename': request_body['filename'],
        'file_content': request_body['file_content']
    }

    return request_body


def find_xlsx_files(directory):
    """Find all xlsx files in a given directory and its subdirectories."""
    xlsx_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".xlsx"):
                xlsx_files.append(os.path.join(root, file))
    return xlsx_files


def read_excel_and_filter(columns_of_interest, skiprows, uploaded_file):
    df = pd.read_excel(uploaded_file, skiprows=skiprows, engine='openpyxl')
    # Select only the columns of interest
    selected_df = df.filter(items=columns_of_interest)
    # Drop rows with all NaN values
    selected_df.dropna(how='all', inplace=True)
    # Reset index after dropping rows
    selected_df.reset_index(drop=True, inplace=True)
    # Display the resulting DataFrame
    # Print each line of data
    for index, row in selected_df.iterrows():
        print("Line", index + 1)
        for col in selected_df.columns:
            print(f"{col}: {row[col]}")
        print("\n")  # Add a new line between each row
    records = selected_df.to_dict(orient='records')
    return records


def skiprows_read_excel_and_filter(uploaded_file, columns_of_interest):
    skiprows = 1
    # Maximum limit for skiprows
    max_skiprows = 10
    # Try reading the Excel file with increasing values of skiprows
    records = None
    while skiprows <= max_skiprows:

        records = read_excel_and_filter(columns_of_interest, skiprows, uploaded_file)

        if records:
            print("Records extracted successfully with skiprows:", skiprows)
            break
        else:
            print(f"No records extracted with skiprows {skiprows}. Trying with skiprows {skiprows + 1}.")
            skiprows += 1
    # logger.info(f"Catalog Extracted:  {len(records)}", extra={"count": len(records)})
    # print(f"Catalog Extracted:  {len(records)}")
    return records

