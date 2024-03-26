import subprocess
import schedule
import threading
import time

def run_python_files():
    # List of Python files to execute
    python_files = ['mergeVideo.py', 'mergeGpx.py', 'map.py']

    # Iterate through the list and execute each Python file
    for python_file in python_files:
        print(f"Executing {python_file}...")
        subprocess.run(['python', python_file], check=True)
        print(f"{python_file} executed successfully.")

def run_main():
    # Run main.py
    subprocess.run(['python', 'main.py'], check=True)

def main():
    # Schedule the execution of Python files every 15 minutes
    schedule.every(15).minutes.do(run_python_files)

    # Run the Python files immediately
    run_python_files()

    # Run main.py in a separate thread
    main_thread = threading.Thread(target=run_main)
    main_thread.start()

    # Keep the script running to allow schedule to continue working
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

if __name__ == "__main__":
    main()
