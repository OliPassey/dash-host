import os
import subprocess
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory
import threading
import glob
import gpxpy

app = Flask(__name__)

# Set the directory for uploaded videos
app.config['UPLOAD_FOLDER'] = './static/in'
app.config['PROCESSED_FOLDER'] = './static/videos'
app.config['GPX_FOLDER'] = './static/in'
app.config['GPX_OUT'] = './static/gpx'

def process_videos(video_dir):
    list_file = "file_list.txt"
    os.chdir(video_dir)
    video_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
    video_files.sort()
    
    if not video_files:
        print("No video files found.")
        return
    
    # Extract timestamp from the first file's name
    first_file_name = video_files[0]
    timestamp_str = first_file_name.split(os.sep)[-1].split('.')[0]  # Adjust according to your path separator if needed
    # Assuming filename format is 'YYYY-MM-DD HHh MMm SSs.gpx'
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %Hh %Mm %Ss")
    
    # Format for output filename
    formatted_timestamp = timestamp.strftime("%d-%m-%Y %H-%M-%S")
    # output_file = f"output_{formatted_timestamp}.mp4"  # Explicitly using forward slash
    output_file = f"output_{formatted_timestamp}.mp4"
       
    with open(list_file, 'w') as f:
        for video in video_files:
            f.write(f"file '{video}'\n")
    
    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file,
        '-c', 'copy',
        output_file
    ]
    
    subprocess.run(ffmpeg_cmd, check=True)
    os.remove(list_file)
    
    for video in video_files:
        os.remove(f"{video_dir}/{video}")
    print(f"Concatenation complete. Output file is {output_file}")

    # Move the output file to a different directory
    output_dir = './static/videos'  # Specify the directory where you want to move the file
    os.rename(output_file, os.path.join(output_dir, output_file))
    print(f"Output file moved to {output_dir}")

def merge_gpx_files(input_folder):
    gpx_files = sorted(glob.glob(f"{input_folder}/*.gpx"))
    if not gpx_files:
        print("No GPX files found in the folder.")
        return

    # Extract timestamp from the first file's name
    first_file_name = gpx_files[0]
    timestamp_str = first_file_name.split(os.sep)[-1].split('.')[0]  # Adjust according to your path separator if needed
    # Assuming filename format is 'YYYY-MM-DD HHh MMm SSs.gpx'
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %Hh %Mm %Ss")

    # Format for output filename
    formatted_timestamp = timestamp.strftime("%d-%m-%Y %H-%M-%S")
    output_file = os.path.join(app.config['GPX_OUT'], f"output_{formatted_timestamp}.gpx")

    merged_gpx = gpxpy.gpx.GPX()
    for gpx_file in gpx_files:
        try:
            with open(gpx_file, 'r') as f:
                print(f"Processing {gpx_file}...")
                gpx = gpxpy.parse(f)
                
                for waypoint in gpx.waypoints:
                    merged_gpx.waypoints.append(waypoint)
                
                for route in gpx.routes:
                    merged_gpx.routes.append(route)
                
                for track in gpx.tracks:
                    merged_gpx.tracks.append(track)

        except Exception as e:
            print(f"Error processing {gpx_file}: {e}")
            continue

    with open(output_file, 'w') as f:
        f.write(merged_gpx.to_xml())
        print(f"Merged GPX saved as {output_file}")

@app.route('/')
def index():
    # List video files in the static/videos directory
    videos = os.listdir('./static/videos')
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        # Start video processing in a new thread
        threading.Thread(target=process_videos, args=(app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER'])).start()
        return 'File has been uploaded and processing will start shortly.'

@app.route('/merge_gpx', methods=['POST'])
def merge_gpx():
    # Start merging GPX files in a new thread
    threading.Thread(target=merge_gpx_files, args=(app.config['GPX_FOLDER'],)).start()
    return 'GPX files will be merged shortly.'

@app.route('/merge_mp4', methods=['POST'])
def merge_mp4():
    # Start merging mp4 files in a new thread
    threading.Thread(target=process_videos, args=(app.config['UPLOAD_FOLDER'],)).start()
    return 'MP4 files will be merged shortly.'

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['PROCESSED_FOLDER']):
        os.makedirs(app.config['PROCESSED_FOLDER'])
    app.run(debug=True)
