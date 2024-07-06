from tkinter import filedialog, Tk, Label, Button
import pandas as pd
import numpy as np 
import openai
from dotenv import load_dotenv
import os
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




def get_file_type (filepath):
    return filepath.split(".")[-1]

#accomodtae other file types
# use username
def get_file_details(filepath):
    ext = get_file_type(filepath)
    # username = input("Username: ")
    if ext == "csv":
        df = pd.read_csv(filepath)
    elif ext == "xlsx":
        df = pd.read_excel(filepath)
    elif ext == "json":
        df = pd.read_json(filepath)
    
    shape = df.shape
    column_names = df.columns
    print(f"The uploaded file type is {ext}")
    print(f"Shape of the dataset is: ",shape)
    
    i = 1
    print("These are the columns in the dataset:")
    for column in column_names:
        print(f"{i}. {column}. ")
        i+=1
    
    # print(f"You have opened {ext} file type.\nShape  :{shape} \ncolumn names : {column_names}")
    return df
    



def summary(df):
    gpt_client = openai.Client(api_key=OPENAI_API_KEY)
    response = gpt_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Summarise the dataset in 3 lines, passing you the first five rows which are {df.head(5)}.",
            }
        ],
       #model="gpt-3.5-turbo",
        model="gpt-4o",
    )
    print("\nHere is the summary of the dataset: ")
    print (response.choices[0].message.content)
# step 3 

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
    Q1 = df[numeric_cols].quantile(0.25)
    Q3 = df[numeric_cols].quantile(0.75)
    IQR = Q3 - Q1
    cleaned_df = df[~((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    return cleaned_df

def custom_cleaning(df):
    # Placeholder for custom cleaning logic
    cleaned_df = df  # Replace with actual custom cleaning steps
    return cleaned_df

def cleaning(df):
    options = {
        1: 'Remove Null values',
        2: 'Remove Duplicates',
        3: 'Remove Outliers',
        4: 'Custom Data Cleaning',
        5: 'Exit'
    }
    print("Let us start with Data Cleaning.")
    while True:
        print("Choose from the following data cleaning options:")
        for key, value in options.items():
            print(f"{key}. {value}")
        
        choice = int(input("Enter your choice: "))
        
        if choice not in options:
            print("Invalid choice. Please try again.")
            continue
        
        if choice == 1:
            df = remove_null_values(df)
            print("Null values removed.")
        elif choice == 2:
            df = remove_duplicates(df)
            print("Removed Duplicates.")
        elif choice == 3:
            df = remove_outliers(df)
            print("Outliers Removed")
        elif choice == 5:
            print("Data cleaning complete.")
            break
        elif choice == 4:
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
    # print("\nFinal cleaned DataFrame:")
    # print(df)
    
    return df

def remove_columns(df):
    cols = df.columns
    print("\n Select the columns from below which you wish to delete.")
    i = 1
    for col in cols:
        print(f"{i}. {col}")
        i+=1
    print(f"Press Q to Exit")

    user_input = input("Enter your response: ")
    # "4,5"
    delete_index = user_input.split(",") #["4","5"]
    if delete_index[0] == "Q" or delete_index[0] == "q":
        return df
    
    delete_index = [(int (i))-1 for i in delete_index]
    print(delete_index)
    df.drop(df.columns[delete_index], axis=1, inplace=True)
    df.to_csv ("removed_columns.csv")
    print("\nColumns removed.")
    return df


def consistency(col_name):
    l = []
    for rows in df[col_name]:
        l.append(type(rows))

    # print(type(rows), rows)
    s = set(s)
    if len(list(s)) == 1:
        return False, s
    else:
        return True, s
       

def check_consistency(df):
    cols = df.columns
    # for col in cols:



file_path = select_file()
dataframe = get_file_details(filepath=file_path)
summary(dataframe)
df = remove_columns(dataframe)
df = cleaning (dataframe)   



