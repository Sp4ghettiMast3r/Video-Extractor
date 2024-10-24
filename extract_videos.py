import os
import platform
import subprocess
import zipfile
import patool
import requests

# Function to check and install required packages
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_requirements():
    requirements = ['pyunpack', 'patool', 'requests']
    for package in requirements:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            install(package)

def check_for_updates():
    repo_url = "https://api.github.com/repos/Sp4ghettiMast3r/Video-Extractor/releases/latest"
    try:
        response = requests.get(repo_url)
        latest_version = response.json()['tag_name']
        
        # Assume the current version is stored in a variable
        current_version = "1.0.0"  # Update this with your current version
        if current_version != latest_version:
            print(f"A new version {latest_version} is available!")
        else:
            print("You are using the latest version.")
    except Exception as e:
        print(f"Could not check for updates: {e}")

def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def extract_video_files(archive_path, extract_to):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')
    extracted_files = []

    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.lower().endswith(video_extensions):
                        print(f'Extracting {file_info.filename}...')
                        zip_ref.extract(file_info, extract_to)
                        extracted_files.append(file_info.filename)
        else:
            patool.extract_archive(archive_path, outdir=extract_to)
            for root, dirs, files in os.walk(extract_to):
                for file in files:
                    if file.lower().endswith(video_extensions):
                        extracted_files.append(file)
                        print(f'Extracted {file} from {archive_path}.')

        if not extracted_files:
            print("No video files found in the archive.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    check_requirements()  # Check and install requirements
    check_for_updates()   # Check for updates

    while True:
        clear_console()

        archive_path = input("Enter the path to the archive file (ZIP, 7Z, RAR, etc.): ")

        if not os.path.isfile(archive_path):
            print("The specified file does not exist.")
            continue
        
        extract_to = input("Enter the destination folder to extract video files: ")

        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        extract_video_files(archive_path, extract_to)
        
        delete_file = input("Do you want to delete the archive file? (y/n): ").strip().lower()
        if delete_file == 'y':
            try:
                os.remove(archive_path)
                print(f"Deleted the file: {archive_path}")
            except Exception as e:
                print(f"Could not delete the file: {e}")

        restart = input("Do you want to restart the script? (y/n): ").strip().lower()
        if restart != 'y':
            break

    print("Goodbye!")

if __name__ == "__main__":
    main()
