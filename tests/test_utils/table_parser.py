import pandas as pd
from bs4 import BeautifulSoup

# Helper classes to assist in testing front-end html rendered table functionality on point_inputs.html page. 
class TableParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self._header_cache = None

    #Returns a list of header names in the table
    def get_headers(self):
        """Returns a list of header names in the table."""
        if self._header_cache is None:
            header_elements = self.soup.select("table#data thead th, table#studentsTable thead th")
            self._header_cache = [h.get_text(strip=True) for h in header_elements]
        return self._header_cache

    # Extracts all values under a given column from the HTML table.
    def extract_column(self, column_name):
        #Returns a list of values. If column is not found, raises ValueError.
        headers = self.get_headers()
        if column_name not in headers:
            raise ValueError(f"Column '{column_name}' not found in table headers: {headers}")
        
        idx = headers.index(column_name)
        rows = self.soup.select("table#data tbody tr, table#studentsTable tbody tr")
        return [
            row.find_all("td")[idx].get_text(strip=True)
            for row in rows if len(row.find_all("td")) > idx
        ]

class AdvancedTableParser:
    def __init__(self, html):
        # Parse the HTML using BeautifulSoup
        self.soup = BeautifulSoup(html, "html.parser")
        # Initialize cache for headers and columns
        self._header_cache = None
        self._column_cache = {}
        #self.table = self.soup.find("table")

    def get_table_as_df(self):
        # Convert HTML table to pandas df
        df = self.get_all_data
        return df
        
    def get_headers(self):
        # Return cached headers if already computed
        if self._header_cache:
            return self._header_cache

        # Find all header elements in the table header row
        header_elements = self.soup.select("table#data thead th, table#studentsTable thead th")

        # Extract text and strip whitespace from each header element
        self._header_cache = [h.get_text(strip=True) for h in header_elements]

        return self._header_cache
    
    def extract_row(self, index):
        # Extract a full row of data by index
        headers = self.get_headers()

        rows = self.soup.select("table#data tbody tr, , table#studentsTable tbody tr")
        
        if index >= len(rows):
            raise IndexError("Row index out of range.")
        cells = rows[index].find_all("td")
        
        return {headers[i]: cells[i].get_text(strip=True) for i in range(len(cells))}

    def get_all_data(self):
        # Convert entire table into a list of row dictionaries
        headers = self.get_headers()

        rows = self.soup.select("table#data tbody tr, table#studentsTable tbody tr")

        return [
            {headers[i]: cell.get_text(strip=True) for i, cell in enumerate(row.find_all("td"))}
            for row in rows
        ]

    def diff_table(self, other):
        # Compare this table to another table data
        self_data = self.get_all_data()

        other_data = other.get_all_data()
        
        return [row for row in self_data if row not in other_data]

    def has_column(self, column_name):
        # Check if a column is present in the headers
        return column_name in self.get_headers()
    
    def get_column_values(self, column_name):
        # Return cached result if available
        if column_name in self._column_cache:
            return self._column_cache[column_name]

        # Validate and find column index
        headers = self.get_headers()
        if column_name not in headers:
            raise ValueError(f"Column '{column_name}' not found in headers: {headers}")
        
        idx = headers.index(column_name)
        
        # Extract rows
        rows = self.soup.select("table#data tbody tr, table#studentsTable tbody tr")

        # Safely extract the column text values
        values = [
            cells[idx].get_text(strip=True)
            for row in rows
            if (cells := row.find_all("td")) and len(cells) > idx
        ]
        if values == None:
            return False

        return values

    def is_column_sorted(self, column_name, reverse=False):
        # Check whether the column values are sorted
        values = self.get_column_values(column_name)
        return values == sorted(values, reverse=reverse)
    







