#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:24:25 2023

@author: rishabhpatni
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def format_dataframes_as_string(dataframes):
    formatted_string = ""
    dataframe_count = 0
    
    for i, df in enumerate(dataframes):
        dataframe_count += 1
        formatted_string += f"DataFrame {dataframe_count}:\n"
        
        # Convert the dataframe to a table format
        table_data = df.values.tolist()
        max_lengths = [max(map(lambda x: len(x) if x is not None else 0, col)) for col in zip(*table_data)]
        formatted_table = []
        
        for row in table_data:
            formatted_row = []
            for j, cell in enumerate(row):
                formatted_cell = cell.ljust(max_lengths[j]) if cell is not None else " " * max_lengths[j]
                formatted_row.append(formatted_cell)
            formatted_table.append(formatted_row)
        
        # Convert the formatted table to a string
        for row in formatted_table:
            formatted_string += " | ".join(row) + "\n"
        
        formatted_string += "\n"
    
    return formatted_string


def extract_data_from_website(url):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the relevant section using CSS selectors or other methods
    section = soup.find('section', class_='col-xs-12 col-md-9 main-section pull-right')
    
    # Extract the important text from the section
    important_text = section.get_text(strip=False)
    
    # Find all the table elements in the HTML
    table_elements = soup.find_all('table')
    
    # Iterate over each table element and insert it into the text
    modified_text = important_text
    dataframe_count = 0
    
    for table in table_elements:
        dataframe_count += 1
        
        # Extract the table data into a list of lists
        table_data = []
        
        # Find all the table rows (tr elements)
        rows = table.find_all('tr')
        
        # Iterate over each row
        for row in rows:
            # Extract the table cells (td or th elements) in the row
            cells = row.find_all(['td', 'th'])
            
            # Extract the text from each cell and add it to the row data
            row_data = [cell.get_text(strip=True) for cell in cells]
            
            # Add the row data to the table data
            table_data.append(row_data)
        
        # Convert the table data into a pandas DataFrame
        df = pd.DataFrame(table_data)
        
        # Format the DataFrame as a string
        formatted_table = format_dataframes_as_string([df])
        
        # Insert the formatted table into the modified text
        modified_text = modified_text.replace(table.get_text(strip=False), formatted_table.replace("DataFrame 1", f"DataFrame {dataframe_count}"))
    
    # Return the modified text with tables incorporated
    return modified_text


def main(website_url):
    data = extract_data_from_website(website_url)
    return data

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    main(website_url)
