"""
Please see "readme.txt" for details.

Program functionality:

1. Extract specific information from a PDF document
2. Chatting with a PDF document

I'm lumping 1/2 into the same set of functions, as they're basically the same.

3. Compare 2 similar PDF documents and output the differences
4. Converting JSON data to structured/tabular format
5. Perform sentiment analysis using NLP techniques on any sample data
"""

import os
import populate_database
import query_data
import create_database
import compare_documents
import json_converter
import sentiment

DATA_PATH = "data/pdfs" # change to wherever your pdfs are


def list_files(path):
    # Check if the provided path exists and is a directory
    if not os.path.isdir(path):
        print(f"The provided path {path} is not a valid directory.")
        return

    # List all files in the directory
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print("Files", files)

    if files:
        for file in files:
            print(file)
    else:
        print(f"No files found in '{path}'.")


def choose_files(path):
    filepath1, filepath2 = None, None
    # Check if the provided path exists and is a directory
    if not os.path.isdir(path):
        print(f"The provided path {path} is not a valid directory.")
        return

    # List all files in the directory
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    if files:
        if len(files) >= 2:
            print("Choose file 1 to compare: ")
            for x in range(0, len(files)):
                print(str(x) + " : " + files[x])
            choice = int(input("Enter file choice here: "))
            filepath1 = files[choice]

            files.pop(choice)

            print("Choose file 2 to compare: ")
            for x in range(0, len(files)):
                print(str(x) + " : " + files[x])
            choice = int(input("Enter file choice here: "))
            filepath2 = files[choice]

    else:
        print(f"No files found in '{path}' or number of files insufficient.")

    return filepath1, filepath2


def print_menu():
    print("\nMenu:")
    print("1. Extract specific information from a PDF document\n2. Compare 2 similar PDF documents and output the differences\n3. Converting JSON data to structured/tabular format\n4. Perform sentiment analysis using NLP techniques on any sample data")


def handle_option(option):
    print(f"\nYou chose Option {option}.")
    while True:
        if option == '1':
            print("Creating vector database on the following files: ")
            list_files(DATA_PATH)
            populate_database.main()
            user_input = None
            while user_input != '0':
                user_input = input("Please enter a query to chat with the documents above or 0 to exit: ")
                if user_input != '0':
                    query_data.query_rag(user_input)
        elif option == '2':
            file1, file2 = choose_files(DATA_PATH)
            create_database.main(DATA_PATH + "/" + file1, "db1")
            create_database.main(DATA_PATH + "/" + file2, "db2")
            user_input = None
            while user_input != '0':
                user_input = input("Please enter a query to chat with the documents above or 0 to exit: ")
                if user_input != '0':
                    compare_documents.subquery_generator(file1, file2, user_input)
        elif option == '3':
            user_input = None
            while user_input != '0':
                user_input = input("Please enter a JSON string or 0 to exit: ")
                if user_input != '0':
                    json_converter.main(user_input)
                    print("Created .csv file for JSON string.")

        elif option == '4':
            user_input = None
            while user_input != '0':
                user_input = input("Please enter a sentence or 0 to exit: ")
                if user_input != '0':
                    sentiment.main(user_input)

        break


def main():
    while True:
        print_menu()
        user_choice = input("Please select an option (0 to exit the program): ")

        if user_choice == '0':
            print("Exiting the program. Goodbye!")
            break
        elif user_choice in ['1', '2', '3', '4']:
            handle_option(user_choice)
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
