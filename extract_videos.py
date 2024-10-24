import zipfile
import os
import platform

def clear_console():
    # Clear console based on the operating system
    if platform.system() == 'Windows':
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For macOS/Linux

def extract_video_files(zip_path, extract_to):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')
    extracted_files = []

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.lower().endswith(video_extensions):
                    print(f'Extracting {file_info.filename}...')
                    zip_ref.extract(file_info, extract_to)
                    extracted_files.append(file_info.filename)

        if not extracted_files:
            print("No video files found in the ZIP archive.")
    except zipfile.BadZipFile:
        print("Error: The file is not a valid ZIP file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        clear_console()  # Clear the console at the start of each loop

        zip_path = input("Enter the path to the ZIP file: ")

        if not os.path.isfile(zip_path):
            print("The specified file does not exist.")
            continue  # Restart the loop
        
        extract_to = input("Enter the destination folder to extract video files: ")

        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        extract_video_files(zip_path, extract_to)
        
        delete_file = input("Do you want to delete the ZIP file? (y/n): ").strip().lower()
        if delete_file == 'y':
            try:
                os.remove(zip_path)
                print(f"Deleted the file: {zip_path}")
            except Exception as e:
                print(f"Could not delete the file: {e}")

        restart = input("Do you want to restart the script? (y/n): ").strip().lower()
        if restart != 'y':
            break

    print("Goodbye!")

if __name__ == "__main__":
    main()
