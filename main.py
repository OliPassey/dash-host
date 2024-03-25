import os
import shutil  
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Get list of files in the /processed folder
    processed_folder = './processed'
    
    # Move files from /processed to /static
    for file in os.listdir(processed_folder):
        src = os.path.join(processed_folder, file)
        dst = os.path.join('./static', file)
        shutil.move(src, dst)
    
    # Get updated list of files in /static
    static_files = [file for file in os.listdir('./static')]

    # Group HTML and MP4 files with identical filenames as pairs
    file_pairs = []
    for file in static_files:
        if file.endswith('.html'):
            mp4_file = file.split('.')[0] + '.mp4'
            if mp4_file in static_files:
                file_pairs.append({'html': file, 'mp4': mp4_file})
    
    # Render the template with the list of pairs
    return render_template('index.html', file_pairs=file_pairs)

if __name__ == '__main__':
    app.run(debug=True)
