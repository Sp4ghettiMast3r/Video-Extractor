import os
import platform
import subprocess
import zipfile
import py7zr
import requests
import sys

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_requirements():
    requirements = ['pyunpack', 'requests', 'py7zr']
    for package in requirements:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            install(package)

def check_for_updates(current_version="1.0.1"):
    repo_url = "https://api.github.com/repos/Sp4ghettiMast3r/Video-Extractor/releases/latest"
    try:
        response = requests.get(repo_url)
        latest_version = response.json()['tag_name']
        if current_version != latest_version:
            print(f"A new version {latest_version} is available!")
        else:
            print("You are using the latest version.")
    except Exception as e:
        print(f"Could not check for updates: {e}")

def clear_console():
    os.system('cls')  # Windows command to clear the console

def extract_video_files(archive_path, extract_to):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')
    extracted_files = []

    try:
        if archive_path.lower().endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.lower().endswith(video_extensions):
                        print(f'Extracting {file_info.filename}...')
                        zip_ref.extract(file_info, extract_to)
                        extracted_files.append(file_info.filename)
        elif archive_path.lower().endswith('.7z'):
            with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                archive.extractall(path=extract_to)
                for root, dirs, files in os.walk(extract_to):
                    for file in files:
                        if file.lower().endswith(video_extensions):
                            extracted_files.append(file)
                            print(f'Extracted {file} from {archive_path}.')
        else:
            print("Unsupported archive format.")
            return

        if extracted_files:
            print("Extracted video files:")
            for file in extracted_files:
                print(f" - {file}")
        else:
            print("No video files found in the archive.")
    except Exception as e:
        print(f"An error occurred while extracting: {e}")

def main():
    try:
        check_requirements()
        check_for_updates()

        while True:
            clear_console()

            archive_path = input("Enter the path to the archive file (ZIP, 7Z, etc.): ")
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

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press Enter to close the window...")

if __name__ == "__main__":
    main()
