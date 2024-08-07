"""
Program Name: PMAR_Breakdowns
Author: Timothy Colledge
Date: July 30, 2024 | Most Recent Update: July 30, 2024
Version: 1.5

Description:
This Library serves as a support file for IVZ python scipts. It contains functions and classes that are utilized in data processing for PMAR FI analytics. 

For use of this library please ensure the following installs are completed:
- Ensure Python 3.x is installed.
- Ensure the following Libraries are installed:
    pandas - to install: <pip install pandas> in cmd
    matplotlib - to install: <pip install matplotlib> in cmd
    numpy  - to install: <pip install numpy> in cmd

Disclaimer:
This program is developed for Invesco internal use and authorized 3rd parties only.

"""



import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import re
import numpy as np
import tkinter as tk
from tkinter import filedialog

def take_input(prompt):
    """
    takes used input and casts datatype

    Parameters
    ----------
    prompt : question/prompt for user

    Returns
    -------
    user_input : user input as str or int

    """
    user_input = input(prompt)

    try:
        user_input = int(user_input)
    except ValueError:
        user_input = user_input
    return user_input

def select_folder(Header="Selection"):
    print(Header)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title=Header)
    return folder_path

def select_file(Header="Selection"):
    print(Header)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title=Header)
    return file_path

def get_yes_no_input(prompt_message):
    '''
    Prompts the user for a 'y' or 'n' response. Repeats the prompt if the input is invalid.

    Parameters:
    prompt_message (str): The message to display when asking for input.

    Returns:
    str: 'y' for yes, 'n' for no.
    '''
    while True:
        user_input = input(prompt_message).strip().lower()  # Get input, remove leading/trailing spaces, and convert to lowercase
        if user_input == 'y' or user_input == 'Y':
            return 'y'
        elif user_input == 'n' or user_input == 'N':
            return 'n'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def export_to_excel(filename, **dfs):
    """
    Export multiple DataFrames to an Excel file with each DataFrame in its own sheet.
    
    Args:
    filename (str): The name of the Excel file to export.
    **dfs: Variable number of keyword arguments, where the key is the sheet name and the value is the DataFrame.
    """
    with pd.ExcelWriter(filename, engine = 'xlsxwriter') as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name = sheet_name, index = False)

def import_excel_to_dataframes(file_path):
    """
    Imports Excel Files and puts into Dataframe Series

    Parameters
    ----------
    file_path : excel file to extract data from

    Returns
    -------
    dfs : dataframe series containing all of the sheets in the file

    """
    xls = pd.ExcelFile(file_path)
    dfs = {}
    for sheet_name in xls.sheet_names:
        dfs[sheet_name] = pd.read_excel(xls, sheet_name)

    return dfs

def find_unique_values(df, column_name):
    """
    Function to find unique values in a specific column of a pandas DataFrame.
    
    Parameters:
    - df: pandas DataFrame
    - column_name: str, name of the column in which to find unique values
    
    Returns:
    - unique_values: list of unique values found in the specified column
    """
    unique_values = df[column_name].unique().tolist()
    return unique_values

def build_high_low(df, column_name):
    """
    Returns 2 dataframes containing the highest and lowest values within specified column

    Parameters
    ----------
    df : dataframe from which data is sourced
    column_name : column in df which data is used

    Returns
    -------
    high_df : highest 5 values in df based on specified column
    low_df : lowest 5 values in df based on specified column

    """
    df = df.sort_values(by = column_name, ascending = False)
    high_df = df.head(10)

    df = df.sort_values(by = column_name, ascending = True)

    low_df = df.head(10)
    df = pd.concat([df.head(10),df.tail(10)])

    return high_df, low_df, df

def find_value_index(df, value):
    """
    Find the index (row and column) of a particular data value in a pandas DataFrame.

    Parameters:
    - df: pandas DataFrame
    - value: value to search for in the DataFrame

    Returns:
    - row: row index where the value is found
    - col: column index where the value is found
    """
    # Initialize variables to store row and column indices
    row = None
    col = None

    # Iterate over each column in the DataFrame
    for idx, col_name in enumerate(df.columns):
        # Check if the value is in the current column
        if value in df[col_name].values:
            # Get the row index where the value is found in the current column
            row = df.index[df[col_name] == value][0]  # Assuming the first occurrence is sufficient
            col = idx
            break  # Stop searching once the value is found

    return row, col

def get_export_data_BRA(df):
    """
    Extract specific data from a DataFrame based on predefined search values.

    Parameters:
    - df: pandas DataFrame

    Returns:
    - export_data_names: list of data corresponding to search values (names)
    - export_data_values: list of data corresponding to search values (values)
    """
    export_data_names = []  # Initialize an empty list to store names
    export_data_values = []  # Initialize an empty list to store values
    search_values = ['Portfolio Full Name', 'Portfolio Short Name', 'Date', 'Currency', 'Benchmark']  # Define search values

    # Iterate through each search value
    for value in search_values:
        # Find the row and column index of the current search value in the DataFrame
        row, col = find_value_index(df, value)

        # Append the corresponding name and value to the export lists
        export_data_names.append(df.iloc[row, col])  # Append the name corresponding to the search value
        export_data_values.append(df.iloc[row, col + 1])  # Append the value next to the search value

    return export_data_names, export_data_values  # Return the lists of names and values

def merge_columns(df1, df2, column_name):
    """
    Merges df1 and df2 with df2 column being the filter
    
    Parameters
    ----------
    df1 : first dataframe that will be filtered in the merge
    df2 : second dataframe thats column is used as the filter
    column_name : column in df2 used as filter

    Returns
    -------
    merged_df : filtered dataframe containing only rows in df1 that have same values as in df2's column_name column

    """
    merged_df = pd.merge(df1, df2[[column_name]], how = 'inner', on = column_name)

    return merged_df

def move_column_to_front(df, *column_names):
    """
    Move specified columns to the front of the DataFrame columns in the given order.

    Args:
    - df (pandas.DataFrame): The DataFrame to modify.
    - *column_names (str): Variable number of column names to move to the front.

    Returns:
    - pandas.DataFrame: A new DataFrame with the specified columns moved to the front in the given order.
    """
    # Ensure all specified columns exist in the DataFrame
    for col in column_names:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame.")

    # Get list of columns excluding the specified ones
    remaining_columns = [col for col in df.columns if col not in column_names]

    # Create new list of columns with specified columns moved to the front in order
    new_columns = list(column_names) + remaining_columns

    # Create new DataFrame with columns in the new order
    new_df = df[new_columns].copy()  # Use .copy() to avoid modifying the original DataFrame

    return new_df

def export_dataframe_series_to_pdf(df_series, output_filename):
    """
    Export a series of DataFrames to a PDF file with titles based on variable names.
    
    Args:
    df_series (Series): A pandas Series containing DataFrames with variable names as keys.
    output_filename (str): Output PDF filename.
    """
    with PdfPages(output_filename) as pdf:
        for df_name, df in df_series.items():
            plt.figure(figsize = (8, 6))
            plt.axis('off')
            table = plt.table(cellText = df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x).values,
                              colLabels = df.columns,
                              loc = 'center',
                              cellLoc = 'left',
                              colWidths = [0.15] * len(df.columns))  # Adjust column widths
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.auto_set_column_width([i for i in range(len(df.columns))])
            table.set_fontsize(10)
            for (i, j), cell in table.get_celld().items():
                if i == 0:
                    cell.set_text_props(weight = 'bold', color = 'black')  # Bold and black header cells
                else:
                    cell.set_facecolor('darkblue' if (i + 1) % 2 == 0 else 'grey')  # Set background color
                    cell.set_text_props(color = 'white')  # White font color for non-header cells
            plt.title(df_name)
            pdf.savefig()
            plt.close()


def dataframe_to_dict(df, key_column):
    """
   
    Convert a pandas DataFrame into a dictionary of dictionaries.

    Args:
    - df (pandas.DataFrame): The DataFrame to convert.
    - key_column (str): The name of the column to use as keys in the resulting dictionary.

    Returns:
    - dict: A dictionary where each key is a unique value from the specified key_column.
            The corresponding value for each key is another dictionary where keys are column names
            (excluding the key_column) and values are the corresponding cell values from the DataFrame.

    """
    result_dict = {}

    for index, row in df.iterrows():
        key_value = row[key_column]
        row_dict = {col: row[col] for col in df.columns if col != key_column}

        if key_value not in result_dict:
            result_dict[key_value] = [row_dict]
        else:
            result_dict[key_value].append(row_dict)

    return result_dict


def filter_df_by_string(df, search_string, column_name):
    """
    Filter rows of a DataFrame based on whether a specified string is present in a specified column.
    
    Args:
    df (DataFrame): The input DataFrame.
    search_string (str): The string to search for.
    column_name (str): The name of the column to search in.
    
    Returns:
    DataFrame: DataFrame containing rows where the search string is present in the specified column.
    """
    filtered_df = df[df[column_name].str.contains(search_string, na = False, case = False, regex = True)]
    return filtered_df


def filter_df_by_int(df, search_int, column_name):
    """
    Filter rows of a DataFrame based on whether a specified string is present in a specified column.
    
    Args:
    df (DataFrame): The input DataFrame.
    search_int (int): The int to search for.
    column_name (str): The name of the column to search in.
    
    Returns:
    DataFrame: DataFrame containing rows where the search int is present in the specified column.
    """
    filtered_df = df[df[column_name] == search_int]
    return filtered_df


def read_in_excel_alladin(file_name, sheet_number):
    """
    Reads in excel file and specified sheet

    Parameters
    ----------
    file_name : excel file used
    sheet_number : sheet in excel file

    Returns
    -------
    df : dataframe of sheet

    """
    df = pd.read_excel(file_name, sheet_name = sheet_number)

    description_row_index = -1
    for index, row in df.iterrows():
        if any(re.search(r'description', str(cell), re.IGNORECASE) for cell in row):
            description_row_index = index
            break

    if description_row_index != -1:
        df.columns = df.iloc[description_row_index]
        df = df.iloc[description_row_index + 1:]
    else:
        print("'description' row not found. Returning DataFrame without changes.")
    return df

def read_in_excel_CRD(file_name, sheet_number):
    """
    Reads in excel file and specified sheet

    Parameters
    ----------
    file_name : excel file used
    sheet_number : sheet in excel file

    Returns
    -------
    df : dataframe of sheet

    """
    df = pd.read_excel(file_name, sheet_name = sheet_number)

    return df


def find_first_named_column_index(df):
    """
    Finds The Column index that holds the security name

    Parameters
    ----------
    df : Dataframe being modified into Aladdin Format
    
    Returns
    -------
    i : The Column index that holds the security name

    """
    for i, column in enumerate(df.columns[1:], start = 1):
        if not column.startswith('Unnamed'):
            return i
    return None


def name_filters(df, stop_col):
    """
    Names all Filters respective levels

    Parameters
    ----------
    df : Dataframe being modified into Aladdin Format
    stop_col : The Column index that holds the security name

    Returns
    -------
    df : Dataframe being modified into Aladdin Format

    """
    column_names = df.columns

    for i in range(stop_col):

        column_index = str(i)
        new_column_name = 'Filter Level ' + column_index

        if i == 0:
            old_column_name = column_names[i]
            df = df.rename(columns = {old_column_name: 'Description'})

        if i < len(column_names) and i != 0:
            old_column_name = column_names[i]
            df = df.rename(columns = {old_column_name: new_column_name})

    return df

def find_value_row(df, column_name, value):
    for index in df.index:
        val = df.loc[index, column_name]
        if value == val:
            return index
    
def build_filters(df, stop_col):
    """
    Builds out the filters at each level to appear in the same format as Aladdin

    Parameters
    ----------
    df : Dataframe being modified into Aladdin Format
    stop_col : TThe Column index that holds the security name

    Returns
    -------
    df : Dataframe being modified into Aladdin Format

    """
    row_count = 0
    for row in df.values:
        if pd.isna(row[0]):
            for i in range(stop_col):
                if pd.isna(row[i]):
                    continue
                else:
                    df.iloc[row_count, 0] = row[i]
                    break

        for i in range(1, stop_col):
            if pd.isna(row[i]):
                continue
            else:
                found_new = True
                for n in range(row_count, len(df)):
                    if pd.isna(df.iloc[n, i]):
                        df.iloc[n, i] = df.iloc[row_count, i]
                    elif found_new:
                        found_new = False
                    else:
                        break
        for i in range(1, stop_col):
            if df.iloc[row_count, i] == df.iloc[row_count, 0]:
                df.iloc[row_count, stop_col] = i
                if i == stop_col - 1:
                    df.iloc[row_count, stop_col] = 0
        row_count = row_count + 1

    df = name_filters(df, stop_col)

    df.drop(df.columns[stop_col - 1], axis = 1, inplace = True)

    return df


def alladinize(df):
    """
    Transforms CRD format excel export into Aladdin format

    Parameters
    ----------
    df : Dataframe being modified into Aladdin Format


    Returns
    -------
    df : Dataframe modified into Aladdin Format


    """
    df = df.iloc[1:]
    df_security_name_col = find_first_named_column_index(df)
    df.insert(df_security_name_col, 'Level', np.nan)
    df = build_filters(df, df_security_name_col)

    return df


class IVZ_pd:
    def __init__(self, path, source, type='excel', convert=True, sheet_number=0):        
        if source == 'CRD' or source == 'Workbench':
            self.df = pd.read_excel(path, sheet_name = sheet_number)
            if convert:
                self.df = alladinize(self.df)
    
        elif source == 'Blackrock' or source == 'BRA' or source == 'Explore':
            self.df = pd.read_excel(path, sheet_name = sheet_number)
            description_row_index = -1
            for index, row in self.df.iterrows():
                if any(re.search(r'description', str(cell), re.IGNORECASE) for cell in row):
                    description_row_index = index
                    break
            if description_row_index != -1:
                self.df.columns = self.df.iloc[description_row_index]
                self.df = self.df.iloc[description_row_index + 1:]
            else:
                raise ValueError("No Description Row Found in BRA File")
            
        elif source == 'MSCI':
            self.dfs = import_excel_to_dataframes(path)

        else:
            raise ValueError("Did Not Provide valid file source. Please provide: ['CRD','BRA','MSCI']")


class IVZ_formats: 
    def __init__(self, worksheet):         
        self.header_format = worksheet.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'top',
            'fg_color': '#0070C0',
            'border': 0,
            'font_color': 'white'})
        self.sub_header_format = worksheet.add_format({
            'bold': False,
            'align': 'center',
            'valign': 'top',
            'fg_color': '#808080',
            'border': 0,
            'font_color': 'white',
            'text_wrap': False,
            'num_format': 2
            })

        # set General format
        self.format_general = worksheet.add_format({'border': 1})
        self.format_general.set_num_format(0)  # 0 means general
        self.format_general.set_font_size(12)

        # set integer format "0"
        self.format_integer = worksheet.add_format({'border': 1})
        self.format_integer.set_num_format(1)
        self.format_integer.set_font_size(12)

        # set float format "0.00"
        self.format_float = worksheet.add_format({'border': 1, 'text_wrap': False})
        self.format_float.set_num_format(2)
        self.format_float.set_font_size(12)

        # set integer format with thousands separators "#,##0"
        self.format_integer_separator = worksheet.add_format({'border': 1})
        self.format_integer_separator.set_num_format(3)
        self.format_integer_separator.set_font_size(12)

        # set percent format "0.00%"
        self.format_percent = worksheet.add_format({'border': 1})
        self.format_percent.set_num_format(10)
        self.format_percent.set_font_size(12)
       
class sheet:

    def __init__(self, workbook, name):
        # set General format
        
        # Check if worksheet name already exists
        if name in workbook.sheetnames:
            raise ValueError(f"Worksheet named '{name}' already exists.")

        # Create formats only once per workbook
        if not hasattr(workbook, 'formats_initialized'):
            # set General format
            self.format_general = workbook.add_format({'border': 1})
            self.format_general.set_num_format(0)  # 0 means general
            self.format_general.set_font_size(12)

            # set float format "0.00"
            self.format_float = workbook.add_format({'border': 1, 'text_wrap': False})
            self.format_float.set_num_format(2)
            self.format_float.set_font_size(12)

            workbook.formats_initialized = True
        else:
            self.holder = 0
            # self.format_general = workbook.format_general
            # self.format_float = workbook.format_float
            

        self.sheet = workbook.add_worksheet(name)
    
    def convert_to_excel_coordinates(self, row, col):
        # Calculate column letter (A-Z, AA, AB, ..., AZ, BA, BB, ..., ZZ, AAA, ...)
        col_letter = ''
        while col >= 0:
            col_letter = chr(col % 26 + ord('A')) + col_letter
            col = col // 26 - 1

        # Convert row index to 1-based index (Excel convention)
        row_number = row + 1

        # Combine column letter and row number
        excel_coordinates = f"{col_letter}{row_number}"

        return excel_coordinates

    def merge_cell(self, row1, col1, row2, col2, text, format = None):
        cordinates = self.convert_to_excel_coordinates(row1, col1) + ':' +  self.convert_to_excel_coordinates(row2, col2)
        if format == None:
            self.sheet.merge_range(cordinates, text, self.format_float)
        else:
            self.sheet.merge_range(cordinates, text, format)        

    def fill_cell(self, row, col, text, format = None):
        cordinates = self.convert_to_excel_coordinates(row, col)
        if format == None:
            self.sheet.write(cordinates, text, self.format_float)
        else:
            self.sheet.write(cordinates, text, format)
    
    def write_column(self, row, col, data, format = None):
        if format == None:
            self.sheet.write_column(row, col, data, self.format_float)
        else:
            self.sheet.write_column(row, col, data, format)

# class excel_workbook:
#     def __init__(self, path):
        