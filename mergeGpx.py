import os
import gpxpy
import gpxpy.gpx
import glob
from datetime import datetime

def merge_gpx_files(input_folder):
    gpx_files = sorted(glob.glob(f"{input_folder}/*.gpx"))
    if not gpx_files:
        print("No GPX files found in the folder.")
        return

    # Extract timestamp from the first file's name
    first_file_name = gpx_files[0]
    timestamp_str = first_file_name.split('\\')[-1].split('.')[0]  # Adjust according to your path separator if needed
    # Assuming filename format is 'YYYY-MM-DD HHh MMm SSs.gpx'
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %Hh %Mm %Ss")

    # Format for output filename
    formatted_timestamp = timestamp.strftime("%d-%m-%Y %H-%M-%S")
    output_file = f"processed/output_{formatted_timestamp}.gpx"

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

    # If the concatenation is successful, delete the original files
    if os.path.exists(output_file):
        for gpx in gpx_files:
            os.remove(gpx)
        print("All original gpx files have been deleted.")

input_folder = 'in'
merge_gpx_files(input_folder)
