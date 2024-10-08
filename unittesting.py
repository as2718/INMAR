import pytest
import pandas as pd
from module2 import validate_phone_number, clean_address, split_contact_numbers, clean_data, export_clean_data, bad_data

# Mock data for testing
mock_data = {
    'url': ['https://example.com', 'https://test.com', None],
    'address': ['123 Fake St', '456 Test Ave', '789 Unknown Blvd'],
    'name': ['Restaurant 1', None, 'Restaurant 3'],
    'rate': ['4.5', '3.9', None],
    'votes': [200, 150, None],
    'phone': ['080 26711192\n\n\n+91 7022268193', '7031123456', None],
    'location': ['Bangalore', 'Chennai', None],
    'rest_type': ['Cafe', 'Bar', ''],
    'dish_liked': ['Pizza', '', 'Burger'],
    'cuisines': ['Italian', 'Chinese', None],
    'reviews_list': ['Good food!', 'Okay service', '']
}

test_path = "C:/Users/Abhishek Srivastav/IdeaProjects/Day-18/INMAR/resources/data_file_20210527182730.csv"

@pytest.fixture
def sample_dataframe():
    """Fixture for sample DataFrame"""
    return pd.DataFrame(mock_data)


# Test validate_phone_number function
def test_validate_phone_number(sample_dataframe):
    phone = '080 26711192\n\n\n+91 7022268193'
    assert validate_phone_number(phone, mock_data) == '080 26711192\n\n\n 7022268193'

    invalid_phone = '1234'
    assert validate_phone_number(invalid_phone, mock_data) == '1234'


# Test clean_address function
def test_clean_address():
    dirty_address = "123 Café St, Apt# 3"
    clean_addr = clean_address(dirty_address)
    assert clean_addr == "123 Caf St Apt 3"


# Test split_contact_numbers function
def test_split_contact_numbers():
    contact_number = "080 26711192\n\n\n+91 7022268193"
    contact1, contact2 = split_contact_numbers(contact_number)
    assert contact1 == "080 26711192"
    assert contact2 == "+91 7022268193"


# Test clean_data function
def test_clean_data(sample_dataframe):
    cleaned_df = clean_data(sample_dataframe)
    assert cleaned_df['address'].apply(lambda x: isinstance(x, str)).all()  # Ensure addresses are cleaned
    assert 'contact number 1' in cleaned_df.columns  # Ensure contact numbers are split
    assert 'contact number 2' in cleaned_df.columns


# Test process_data function
def test_process_data(tmpdir):
    # Create a mock CSV file in a temporary directory
    file_path = tmpdir.join("mock_data.csv")
    sample_df = pd.DataFrame(mock_data)
    sample_df.to_csv(file_path, index=False)

    # Import process_data from data_processing module
    from module2 import process_data,export_clean_data

    cleaned_data = process_data(str(file_path))

    assert len(cleaned_data) > 0  # Ensure that cleaned data is returned

    original_data, correct_data, bad_data = export_clean_data(test_path)

    assert len(correct_data) + len(bad_data) == len(original_data)



