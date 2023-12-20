import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

#NEED imported TETRAX raw data

def process_data(file_path, save_path):
    # Load the data
    data = pd.read_excel(file_path)

    # Identifying the required columns
    required_columns = ['Patient ID', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
                        'WDI', 'ST', 'AB', 'CD', 'AC', 'BD']
    prefixes = ['NO', 'NC', 'PO', 'PC', 'HR', 'HL', 'HB', 'HF']

    # Creating a list of all required columns with prefixes
    all_required_columns = []
    for prefix in prefixes:
        for col in required_columns:
            column_name = f"{prefix} {col}" if col != 'Patient ID' else col
            if column_name in data.columns:
                all_required_columns.append(column_name)

    # Selecting the required columns from the data
    filtered_data = data[all_required_columns]

    # Calculating averages for 'F2-4', 'F5-6', 'F7-8'
    for prefix in prefixes:
        filtered_data[f'{prefix} F2-4'] = filtered_data[[f'{prefix} F2', f'{prefix} F3', f'{prefix} F4']].mean(axis=1)
        filtered_data[f'{prefix} F5-6'] = filtered_data[[f'{prefix} F5', f'{prefix} F6']].mean(axis=1)
        filtered_data[f'{prefix} F7-8'] = filtered_data[[f'{prefix} F7', f'{prefix} F8']].mean(axis=1)

        # Dropping the original 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8' columns
        for col in ['F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']:
            filtered_data.drop(f'{prefix} {col}', axis=1, inplace=True)

    # Reordering columns as requested
    ordered_columns = []
    for prefix in prefixes:
        for col in required_columns:
            if col in ['F2', 'F3', 'F4']:
                new_col = f'{prefix} F2-4'
            elif col in ['F5', 'F6']:
                new_col = f'{prefix} F5-6'
            elif col in ['F7', 'F8']:
                new_col = f'{prefix} F7-8'
            else:
                new_col = f'{prefix} {col}' if col != 'Patient ID' else col

            if new_col not in ordered_columns and new_col in filtered_data.columns:
                ordered_columns.append(new_col)

    reordered_data = filtered_data[ordered_columns]

    # Removing duplicate 'Patient ID' columns except the first one
    reordered_data = reordered_data.loc[:,~reordered_data.columns.duplicated()]

    # Saving the processed data to the specified save path
    output_file_path = f"{save_path}/processed_data.xlsx"
    reordered_data.to_excel(output_file_path, index=False)

    return output_file_path

def gui_select_file_and_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Select Excel file
    file_path = filedialog.askopenfilename(title="Select Excel file", filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        messagebox.showinfo("No File Selected", "You did not select a file.")
        return

    # Select save path
    save_path = filedialog.askdirectory(title="Select Save Directory")
    if not save_path:
        messagebox.showinfo("No Directory Selected", "You did not select a directory.")
        return

    # Process the selected file and save the output
    processed_file_path = process_data(file_path, save_path)
    messagebox.showinfo("Completed", f"Processing completed. File saved to: {processed_file_path}")

# Run the GUI
gui_select_file_and_path()
