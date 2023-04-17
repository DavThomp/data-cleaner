#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import matplotlib.pyplot as plt


MAIN_MENU = """\nPlease choose from the following options:
1 – Load data from a file
2 – View data
3 – Clean data
4 – Analyse data
5 – Visualise data
6 - Save data to a file
7 - Quit"""

SUB_MENU = """\nCleaning data:
1 – Drop rows with missing values
2 – Fill missing values
3 – Drop duplicate rows
4 – Drop column
5 – Rename column
6 - Finish cleaning"""


def main():
    print("Welcome to the Dataframe Statistician!")
    print("Programmed by David Thompson")

    print(MAIN_MENU)
    menu_choice = input(">>> ")
    data_frame = pd.DataFrame()
    while menu_choice != "7":
        if menu_choice == "1":
            data_frame = load_data()
        elif menu_choice == "2":
            print(data_frame)
        elif menu_choice == "3":
            if check_is_data_loaded(data_frame):
                display_sub_menu(data_frame)
        elif menu_choice == "4":
            if check_is_data_loaded(data_frame):
                statistics = calculate_statistics(data_frame)
                correlations = calculate_correlations(data_frame)
                print_report(statistics, correlations)
        elif menu_choice == "5":
            if check_is_data_loaded(data_frame):
                display_chart(data_frame)
        elif menu_choice == "6":
            save_to_file(data_frame)
        else:
            print("Invalid option!")
        print(MAIN_MENU)
        menu_choice = input(">>> ")
    print("Goodbye")

    
def display_sub_menu(data_frame):
    print("Cleaning ...")
    print(data_frame)
    print(SUB_MENU)
    sub_menu_choice = input(">>> ")
    while sub_menu_choice != "6":
        if sub_menu_choice == "1":
            drop_missing_value_rows(data_frame)
        elif sub_menu_choice == "2":
            fill_missing_values(data_frame)
        elif sub_menu_choice == "3":
            drop_duplicate_rows(data_frame)
        elif sub_menu_choice == "4":
            drop_column(data_frame)
        elif sub_menu_choice == "5":
            rename_column(data_frame)
        else:
            print("Invalid option!")
        print(data_frame)
        print(SUB_MENU)
        sub_menu_choice = input(">>> ")  

        
def check_is_data_loaded(data_frame):
    if not data_frame.empty:
        return True
    else:
        print("No data loaded.")
    
            
def load_data():
    file_name = input("Enter a filename: ")
    file_valid = False
    try:
        data_frame = pd.read_csv(file_name)
        file_valid = True
    except FileNotFoundError:
        print("File name invalid.")
    except pd.errors.ParserError:
        print("File format invalid.")
        
    if file_valid:
        print("Data has been loaded successfully.")
        set_index(data_frame)
        return data_frame


def print_columns(data_frame, message):
    print(message)
    for column in data_frame.columns:
            print(f"     {column}")


def set_index(data_frame):
    print_columns(data_frame, "Which column do you want to set as index? (leave blank for none)")
    index = input(">>> ")
    valid_column = False
    while not valid_column and not index == "":
        try:
            data_frame.set_index(index, inplace=True)
            valid_column = True
        except KeyError:
            print_columns(data_frame, "\nEnter a valid column. (leave blank for none)")
            index = input(">>> ")
    print(f"{index} set as index." if not index == "" else "No index set.")
    return data_frame


def drop_missing_value_rows(data_frame):
    threshold = get_valid_integer("Enter the threshold for dropping rows: ", from_integer=0)
    data_frame.dropna(thresh=threshold, inplace=True)
    return data_frame

    
def get_valid_integer(prompt, from_integer):
    valid_input = False
    while not valid_input:
        try: 
            integer = int(input(prompt))
            if integer >= from_integer:
                valid_input = True
            else:
                print("Invalid. Enter a non negative number.")
        except ValueError:
            print("Enter a valid integer.")
        except TypeError:
            print("Enter a valid integer.")    
    return integer


def fill_missing_values(data_frame):
    value = get_valid_float("Enter a replacement value: ")
    data_frame.fillna(value, inplace=True)
    return data_frame


def drop_duplicate_rows(data_frame):
    check_duplicates = data_frame.duplicated().value_counts()
    try:
        count_duplicates = check_duplicates[True]
        data_frame.drop_duplicates(inplace=True)
        print(f"{count_duplicates} rows dropped.")
    except KeyError:
        print("No duplicate rows exist.")
    
    
def get_valid_float(prompt):
    valid_input = False
    while not valid_input:
        try:
            value = float(input(prompt))
            valid_input = True
        except ValueError:
            print("Invalid. Enter a number.")
    return value


def drop_column(data_frame):
    print_columns(data_frame, "Which column do you want to drop? (leave blank for none)")
    column = input(">>> ")
    while column not in data_frame.columns and not column == "":
        print("\nEnter a valid column.")
        print_columns(data_frame, "Which column do you want to drop? (leave blank for none)")
        column = input(">>> ")
    
    if not column == "":
        data_frame.drop(column, axis=1, inplace=True)
    
    return data_frame


def rename_column(data_frame):
    print_columns(data_frame, "Enter the current name of a column to rename: ")
    current_name = input(">>> ")
    while current_name not in data_frame.columns:
        print_columns(data_frame, "\nNot valid. Enter a current name: ")
        current_name = input(">>> ")
        
    new_name = input(f"\nEnter new name for {current_name} (cannot be blank or an existing column name): ")
    while new_name in data_frame.columns or new_name == "":
        new_name = input(f"Not valid. Enter new name for {current_name} (cannot be blank or an existing column name): ")
    
    data_frame.rename(columns={current_name : new_name}, inplace=True)
    return data_frame


def calculate_statistics(data_frame):
    statistics = {}
    for column in data_frame:
        statistics[column] = [data_frame[column].count(),
                              data_frame[column].min(),
                              data_frame[column].max(),
                              data_frame[column].mean(),
                              data_frame[column].median(),
                              data_frame[column].std(),
                              data_frame[column].sem()]
        
    return statistics

    
def calculate_correlations(data_frame):       
    correlations = data_frame.corr()
    return correlations


def print_report(statistics, correlations):
    for key, values in statistics.items():
        title = key
        title_length = len(title)
        number_of_values = values[0]
        maximum = values[1]
        minimum = values[2]
        mean = values[3]
        median = values[4]
        standard_deviation = values[5]
        standard_error = values[6]
                              
        print(f"\n{title}")
        print(f"{'':-<{title_length}}")
        print(f"{'number of values (n):':>22} {number_of_values}")
        print(f"{'minimum:':>22} {maximum:.2f}")
        print(f"{'maximum:':>22} {minimum:.2f}")
        print(f"{'mean:':>22} {mean:.2f}")
        print(f"{'median:':>22} {median:.2f}")
        print(f"{'standard deviation:':>22} {standard_deviation:.2f}")
        print(f"{'std. err. of mean:':>22} {standard_error:.2f}")
    print(f"\n{correlations}")
    
    
def display_chart(data_frame):
    chart_type = get_chart_type()
    has_subplots = get_has_subplots("Do you want to use subplots? (y/n) ")
    title = input("Please enter the title for the plot (leave blank for no title). ")
    x_label = input("Please enter the x-axis label (leave blank for no label). ")
    y_label = input("Please enter the y-axis label (leave blank for no label). ")
    
    plt.figure()
    if chart_type == "line":
        data_frame.plot.line(title=title, xlabel=x_label, ylabel=y_label, subplots=has_subplots)
    elif chart_type == "bar":
        data_frame.plot.bar(title=title, xlabel=x_label, ylabel=y_label, subplots=has_subplots)
    else:
        data_frame.plot.box(title=title, xlabel=x_label, ylabel=y_label, subplots=has_subplots)
    plt.tight_layout()
    
    
def get_chart_type():
    chart_types = ["line", "bar", "box"]
    chart_type = input("Please choose from the following kinds: line, bar, box ")
    while chart_type not in chart_types:
        chart_type = input("Invalid. Please choose from the following kinds: line, bar, box ")
    return chart_type


def get_has_subplots(message):
    yes_or_no = input(message)
    while yes_or_no != "y" and yes_or_no != "n":
        yes_or_no = input("Invalid. Enter yes(y) or no(n). ")
    if yes_or_no == "y":
        return True
    else:
        return False


def save_to_file(data_frame):
    file_name = input("Enter a filename (including extension): ")
    if not file_name == "":
        try:
            is_named_index = check_is_named_index(data_frame)
            data_frame.to_csv(file_name, index=is_named_index)
            print("File saved.")
        except OSError:
            print("The file name or extension entered is invalid.")
    else: 
        print("Cancelled. File not saved.")
        
    
def check_is_named_index(data_frame):
    if not data_frame.index.name is None:
        return True
    else:
        return False
  

    
main()





