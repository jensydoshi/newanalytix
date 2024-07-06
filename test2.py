import pandas as pd
import numpy as np
import openai
from dotenv import load_dotenv
import os
from tkinter import filedialog, Tk, Label, Button

load_dotenv()

# Access variables
OPENAI_API_KEY = os.getenv('API_KEY')
# Initialize filepath as a global variable
filepath = ""

def select_file():
    def browseFiles():
        global filepath  # Declare filepath as global
        filepath = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
        if filepath:
            label_file_explorer.configure(text="File Opened:\n" + filepath)
            window.destroy()  # Close the Tkinter window after selecting the file

    # Create the root window
    window = Tk()

    # Set window title
    window.title('File Explorer')

    # Set window size
    window.geometry("300x150")

    # Set window background color
    window.config(background="black")

    # Create a File Explorer label
    label_file_explorer = Label(window,
                                text="File Explorer",
                                width=20,
                                fg="blue")

    button_explore = Button(window,
                            text="Browse",
                            width=10,
                            command=browseFiles)

    button_exit = Button(window,
                         text="Exit",
                         width=10,
                         command=window.destroy)  # Exit button destroys the window

    # Grid method is chosen for placing
    # the widgets at respective positions
    label_file_explorer.grid(column=1, row=1, padx=10, pady=10)
    button_explore.grid(column=1, row=2, padx=10, pady=10)
    button_exit.grid(column=1, row=3, padx=10, pady=10)

    # Let the window wait for any events
    window.mainloop()

    # Now you can access 'filepath' globally after the Tkinter window is closed
    print("Selected File:", filepath)
    return filepath

def get_file_type(filepath):
    return filepath.split(".")[-1]

def get_file_details(filepath):
    ext = get_file_type(filepath)
    if ext != "json":
        df = pd.read_csv(filepath)
        shape = df.shape
        column_names = df.columns
        print(f"Hi Jenny \nYou have opened {ext} file type.\nShape :{shape} \ncolumn names : {column_names}")
        return df

def summary(df):
    gpt_client = openai.Client(api_key=OPENAI_API_KEY)
    response = gpt_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"summarise the dataset {df.head(5)} ",
            }
        ],
        model="gpt-4o",
    )
    print("\n")
    print(response.choices[0].message.content)

def remove_null_values(df):
    cleaned_df = df.dropna()
    return cleaned_df

def remove_duplicates(df):
    cleaned_df = df.drop_duplicates()
    return cleaned_df

def remove_missing_values(df):
    cleaned_df = df.dropna(how='any')
    return cleaned_df

def remove_outliers(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Calculate Q1, Q3, and IQR for each numeric column
    Q1 = df[numeric_cols].quantile(0.25)
    Q3 = df[numeric_cols].quantile(0.75)
    IQR = Q3 - Q1
    
    # Print the quartiles and IQR for debugging purposes
    print("Q1 (25th percentile):\n", Q1)
    print("Q3 (75th percentile):\n", Q3)
    print("IQR (Interquartile Range):\n", IQR)
    
    # Calculate the lower and upper bounds for each numeric column
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Print the bounds for debugging purposes
    print("Lower Bound:\n", lower_bound)
    print("Upper Bound:\n", upper_bound)
    
    # Identify outliers based on the calculated bounds
    condition = ~((df[numeric_cols] < lower_bound) | (df[numeric_cols] > upper_bound)).any(axis=1)
    
    # Print the condition mask to see which rows are kept
    print("Condition Mask:\n", condition)
    
    # Filter out the outliers
    cleaned_df = df[condition]
    
    # Print the cleaned DataFrame to verify outliers have been removed
    print("Cleaned DataFrame:\n", cleaned_df)
    
    return cleaned_df

def custom_cleaning(df):
    # Placeholder for custom cleaning logic
    cleaned_df = df  # Replace with actual custom cleaning steps
    return cleaned_df

def cleaning(df):
    options = {
        1: 'Remove null values',
        2: 'Remove Duplicates',
        3: 'Remove missing values',
        4: 'Remove outliers',
        5: 'None',
        6: 'Custom Data cleaning'
    }
    
    while True:
        print("Choose from the following cleaning steps:")
        for key, value in options.items():
            print(f"{key}. {value}")
        
        choice = int(input("Enter your choice: "))
        
        if choice not in options:
            print("Invalid choice. Please try again.")
            continue
        
        if choice == 1:
            df = remove_null_values(df)
        elif choice == 2:
            df = remove_duplicates(df)
        elif choice == 3:
            df = remove_missing_values(df)
        elif choice == 4:
            df = remove_outliers(df)
        elif choice == 5:
            print("Data cleaning complete.")
            break
        elif choice == 6:
            df = custom_cleaning(df)
        
        # Save cleaned DataFrame to a file (you can adjust the filename and format as needed)
        df.to_csv('cleaned_data.csv', index=False)  # Saving as CSV for example
        
        # Remove the chosen option from the list of options
        if choice in options:
            del options[choice]
        
        if not options or (len(options) == 1 and 5 in options):
            print("No more cleaning steps available.")
            break
    
    # Display the final cleaned DataFrame
    print("\nFinal cleaned DataFrame:")
    print(df)
    
    return df

file_path = select_file()
dataframe = get_file_details(filepath=file_path)
summary(dataframe)
cleaning(dataframe)
