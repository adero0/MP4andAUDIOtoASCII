# MP4andAUDIOtoASCII

**MP4andAUDIOtoASCII** is a fun mini project of mine that extracts frames from a video file (and optionally syncs with an audio track) to render a **terminal-based ASCII art video**.  
Originally made for just [bad apple!!](https://archive.org/details/TouhouBadApple), but now also supports color.

![alt_text](https://github.com/adero0/MP4andAUDIOtoASCII/blob/main/readme_img.png)

---

## Features

### Core Functionality
- **Frame Extraction** – Converts video frames to ASCII representation.
- **Optional Audio Path** – Accepts an external audio file to sync playback.
- **Terminal Playback** – Displays ASCII video in real-time in your terminal.
- **Video Progress Bar** – Visual indicator of playback position.
- **Playback Controls** – Keyboard shortcuts for:
  - `←` Rewind 10 seconds  
  - `→` Skip forward 10 seconds  
  - `Space` Pause/Play
- **Preprocessing** - The video gets preprocessed and saved as a .txt to allow for smoother animation.

---

## Requirements
  
- Python 3.8+
- Libraries:
  - `opencv-python`
  - `pygame`
  - `keyboard`


## To Run the Program do the following

1. **Download/Copy the source code.**  
2. **Save it as** `<your_name>.py`  
3. **Install required dependencies:**
   ```bash
   pip install opencv-python pygame keyboard
4. **Download your video of choice(and optionally audio path)**
5. **Put all the files in one directory like so:**
   
some_directory_name/

│

├── <your_name>.py,

├── video_file.mp4,

└── audio_file.mp3   (optional)

7. **Now in the terminal of choice cd into some_directory_name and preferably fullscreen the terminal window**
8. **Run python** `<your_name>.py`
