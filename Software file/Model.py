import pandas as pd

INVENTORY_FILE_PATH = r'C:\Users\prata\OneDrive\Documents\Projects\POS-System-Raj\Data\inventory.xlsx'
USERS_FILE_PATH = r'C:\Users\prata\OneDrive\Documents\Projects\POS-System-Raj\Data\users.csv'


def add_item(item_name, item_price, item_quantity):
    inventory_data = pd.read_excel(INVENTORY_FILE_PATH)  # Read the current inventory data from the Excel file
    new_item = pd.DataFrame({
        'Item Name': [item_name],
        'Price': [item_price],
        'Quantity': [item_quantity]
    })
    inventory_data = pd.concat([inventory_data, new_item], ignore_index=True)  # Concatenate the new item to the inventory data
    inventory_data.to_excel(INVENTORY_FILE_PATH, index=False)  # Update the Excel file with the new inventory data


def remove_item(item_name):
    inventory_data = pd.read_excel(INVENTORY_FILE_PATH)  # Read the current inventory data from the Excel file
    inventory_data = inventory_data[inventory_data['Item Name'] != item_name]  # Remove the item from the inventory data
    inventory_data.to_excel(INVENTORY_FILE_PATH, index=False)  # Update the Excel file with the modified inventory data


def get_inventory_data():
    inventory_data = pd.read_excel(INVENTORY_FILE_PATH)  # Read the current inventory data from the Excel file
    return inventory_data.to_dict('records')  # Return the inventory data as a list of dictionaries
