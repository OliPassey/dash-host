# Dash-Host 

## What? 
This is a horrible set of python scripts that takes segmented dashcam footage and merges it back together into one video file. 
The intended work-flow is; 
- Record Dashcam Footage with a GPX file https://play.google.com/store/apps/details?id=com.helge.droiddashcam&pli=1
- Sync the video & GPX files to the /in directory
- Run go.py
- It will merge the video files into one, same with the GPX file. So one journey at a time currently.
- It should look for new files to process every hour, and it will delete incoming files once processed.
- View in browser: http://127.0.0.1:5000/

# Notes 
I plan to dockerize this to make life simple, its not ready yet. 
Its rough around the edges and I want to add more features down the line. 

# Screenshots
![image](https://github.com/OliPassey/dash-host/assets/7745805/6b0cbe8c-196f-484b-b7e9-3452bb41f3a1)
