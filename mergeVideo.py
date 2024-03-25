import os
import subprocess
from datetime import datetime

# Corrected directory path
video_dir = 'in'
# Temporary file list name
list_file = "file_list.txt"

# Fetch all mp4 files from the directory
video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
# Sort the files if needed; this example sorts them by name
video_files.sort()

# Assuming video_files is not empty and sorted, get the timestamp from the first file
if video_files:
    # Extract timestamp from the first file's name
    first_file_name = video_files[0]
    # Assuming filename format is 'YYYY-MM-DD HHh MMm SSs.mp4'
    timestamp_str = first_file_name.split('.')[0]  # Remove the file extension
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %Hh %Mm %Ss")
    # Format this time in the UK date and time format (DD-MM-YYYY HH-MM-SS)
    timestamp = timestamp.strftime("%d-%m-%Y %H-%M-%S")
    # The output file with timestamp, saved one directory level higher
    output_file = f"processed/output_{timestamp}.mp4"
else:
    print("No video files found.")
    exit()


# Create or overwrite the list file with full paths
with open(list_file, 'w') as f:
    for video in video_files:
        # Include the path to the video directory
        f.write(f"file '{os.path.join(video_dir, video)}'\n")

# Build the ffmpeg command with full path for the output
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', list_file,
    '-c', 'copy',
    output_file
]

# Run the ffmpeg command
subprocess.run(ffmpeg_cmd, check=True)

# Optionally, remove the list file after concatenation
os.remove(list_file)

# If the concatenation is successful, delete the original files
if os.path.exists(output_file):
    for video in video_files:
        os.remove(os.path.join(video_dir, video))
    print("All original video files have been deleted.")

print(f"Concatenation complete. Output file is {output_file}")
