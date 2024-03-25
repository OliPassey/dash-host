import gpxpy
import folium
import glob
import os

def plot_gpx_on_map(gpx_file_path, map_output_path):
    # Load and parse the GPX file
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Extract first and last points
    first_point = gpx.tracks[0].segments[0].points[0]
    last_point = gpx.tracks[-1].segments[-1].points[-1]

    # Calculate midpoint
    mid_lat = (first_point.latitude + last_point.latitude) / 2
    mid_lon = (first_point.longitude + last_point.longitude) / 2

    # Initialize the map to the midpoint location
    folium_map = folium.Map(location=[mid_lat, mid_lon], tiles="Cartodb dark_matter", zoom_start=8)

    # Add marker for the first point (green circle)
    folium.Marker(
        location=[first_point.latitude, first_point.longitude],
        popup='Start',
        icon=folium.Icon(color='green', icon='circle')
    ).add_to(folium_map)

    # Add marker for the last point (red circle)
    folium.Marker(
        location=[last_point.latitude, last_point.longitude],
        popup='Finish',
        icon=folium.Icon(color='red', icon='circle')
    ).add_to(folium_map)

    # Loop through all tracks, segments, and points to add them to the map
    for track in gpx.tracks:
        for segment in track.segments:
            points = [(point.latitude, point.longitude) for point in segment.points]
            # Add the points as a line to the map
            folium.PolyLine(points, color="orange", weight=5, opacity=1).add_to(folium_map)

    # Save the map to an HTML file
    folium_map.save(map_output_path)
    print(f"Map has been saved to {map_output_path}")

def process_folder(folder_path):
    # Find all GPX files in the folder
    gpx_files = glob.glob(os.path.join(folder_path, '*.gpx'))
    
    # Loop through each GPX file and create a corresponding HTML file
    for gpx_file in gpx_files:
        html_file_path = os.path.splitext(gpx_file)[0] + '.html' # Change the extension to .html
        plot_gpx_on_map(gpx_file, html_file_path)

# Example usage: Replace 'path/to/your/folder' with your actual folder path containing GPX files
folder_path = 'processed'
process_folder(folder_path)
