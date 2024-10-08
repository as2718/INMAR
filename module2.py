import os
import shutil

import pandas as pd
import re
from variables import ARCHIVE_PATH

bad_data = pd.DataFrame()


def validate_phone_number(in_phone, data):
    """Validate and format phone numbers."""
    global bad_data
    # Define regex patterns for valid phone numbers
    landline_pattern = r'^0[2-9]\d{1,4}\d{6,8}$'
    mobile_pattern = r'^[6-9]\d{9}$'
    in_phone = str(in_phone)

    # Clean phone number by removing "+91" and extra spaces

    phone = str(in_phone.replace("+91", '').strip())
    contact = re.split(r'\s*\n+\s*', str(phone).strip())

    # Check if phone number matches the valid patterns
    if (re.match(landline_pattern, str(contact[0]).replace(' ', ''))
            or re.match(mobile_pattern, str(contact[0]).replace(' ', '') or len(contact[0]) == 0)):

        if len(contact) > 1:
            if (re.match(landline_pattern, str(contact[1]).replace(' ', ''))
                    or re.match(mobile_pattern, str(contact[1]).replace(' ', '') or len(contact[1]) == 0)):
                return phone
            else:
                # Append the invalid record to the bad_data DataFrame
                bad_data = pd.concat([bad_data, pd.DataFrame([data])])
                return phone
    else:
        # Append the invalid record to the bad_data DataFrame
        bad_data = pd.concat([bad_data, pd.DataFrame([data])])
        return phone


def clean_address(address):
    """Clean the address field by removing special and junk characters."""
    if not isinstance(address, str):
        return ''

    return re.sub(r'[^\x00-\x7F\s]|[^a-zA-Z0-9\s]', '', address)  # Retain word characters, spaces


def split_contact_numbers(contact_number):
    """Split contact numbers into two separate fields."""
    numbers = re.split(r'\s*\n+\s*', str(contact_number))
    contact1 = numbers[0].strip() if len(numbers) > 0 else None
    contact2 = numbers[1].strip() if len(numbers) > 1 else None
    return contact1, contact2


def clean_data(data):
    """Clean and validate the data."""
    pd.options.mode.copy_on_write = True

    # 1. Clean phone numbers and validate them
    data['phone'] = data.apply(lambda row: validate_phone_number(row['phone'], row), axis=1)

    # 2. Clean address  field
    data['address'] = data['address'].apply(clean_address)

    # 3. clean reviews_list
    data['reviews_list'] = data['reviews_list'].apply(clean_address)  # Assuming similar cleaning logic

    # 4. Split contact numbers into two fields if needed
    data['contact number 1'], data['contact number 2'] = zip(*data['phone'].apply(split_contact_numbers))

    return data


def process_data(file_path):
    """Process the data from the given file path."""
    global bad_data
    # Load the data
    data = pd.read_csv(file_path, encoding='latin1',
                       usecols=['url', 'address', 'name', 'rate', 'votes', 'phone',
                                'location', 'rest_type', 'dish_liked', 'cuisines',
                                'reviews_list'], quotechar='"', quoting=2)

    # Separate bad records (rows with None in 'phone','name','location')
    bad_records_nulls = data[data['name'].isna() | data['phone'].isna() | data['location'].isna()]

    bad_data = bad_records_nulls
    data_without_null = data[~data.index.isin(bad_data.index)]

    # Clean and validate the data
    cleaned_data = clean_data(data_without_null)

    # Return cleaned data for further processing
    return cleaned_data, data


def export_clean_data(path):
    global bad_data
    cleaned_data, original_data = process_data(path)
    cleaned_data = cleaned_data[['url', 'address', 'name', 'rate', 'votes',
                                 'contact number 1', 'contact number 2', 'location', 'rest_type', 'dish_liked',
                                 'cuisines',
                                 'reviews_list']]
    bad_data['contact number 1'], bad_data['contact number 2'] = zip(
        *bad_data['phone'].apply(split_contact_numbers))
    bad_data = bad_data.drop(columns='phone')
    correct_data = cleaned_data[
        ~cleaned_data.index.isin(bad_data.index)]  # removing all bad records from main dataframe
    file_without_extension = re.sub(r'\.[^.]+$', '', os.path.basename(path))
    correct_data.to_csv(ARCHIVE_PATH + "/" + file_without_extension + ".out", index=False)
    bad_data[['url', 'address', 'name', 'rate', 'votes',
              'contact number 1', 'contact number 2', 'location', 'rest_type', 'dish_liked', 'cuisines',
              'reviews_list']].to_csv(ARCHIVE_PATH + "/" + file_without_extension + ".bad", index=False)
    shutil.move(path, ARCHIVE_PATH)
    print(f"File: {os.path.basename(path)} Processed Successfully\n")

    return original_data, correct_data, bad_data  # returning all these values to perform unit testing
