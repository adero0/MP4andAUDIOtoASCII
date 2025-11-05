import os
import cv2
import time
import pygame
import threading
import keyboard
import sys
import ctypes

VIDEO_PATH = "video_file.mp4"
AUDIO_PATH = "audio_file.mp3"
ASCII_CHARS = "█▓▒░$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'."

if os.name == "nt":
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
#state
is_paused = False
current_frame = 0


def frame_to_ascii(frame, new_width=100):
    """Convert a frame to RGB-colored ASCII using ANSI codes."""
    height, width, _ = frame.shape
    aspect_ratio = width / height
    new_height = int(new_width / aspect_ratio / 2.1)
    resized = cv2.resize(frame, (new_width, new_height))

    ascii_frame = []
    for row in resized:
        line = []
        for pixel in row:
            b, g, r = pixel
            brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
            char = ASCII_CHARS[int(brightness / 255 * (len(ASCII_CHARS) - 1))]
            line.append(f"\033[38;2;{r};{g};{b}m{char}\033[0m")
        ascii_frame.append("".join(line))
    return "\n".join(ascii_frame)


def preprocess_video(video_path, width=100):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: could not open video file.")
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    print(f"Preprocessing {total_frames} frames...")

    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        ascii_frame = frame_to_ascii(frame, new_width=width)
        frames.append(ascii_frame)
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{total_frames} frames...", end="\r")

    cap.release()
    print(f"\n✅ Done preprocessing {len(frames)} frames.")
    return frames


def save_preprocessed_frames(frames, video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_name = f"preprocessed_{base_name}.txt"
    with open(output_name, "w", encoding="utf-8") as f:
        f.write("<<<FRAME_END>>>".join(frames))
    print(f"✅ Saved preprocessed frames to '{output_name}'")


def load_preprocessed_frames(video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    file_name = f"preprocessed_{base_name}.txt"
    if not os.path.exists(file_name):
        return None
    print(f"Loading preprocessed frames from '{file_name}'...")
    with open(file_name, "r", encoding="utf-8") as f:
        data = f.read()
    frames = data.split("<<<FRAME_END>>>")
    print(f"✅ Loaded {len(frames)} frames from file.")
    return frames


def play_audio():
    """Play the audio file using pygame."""
    if not os.path.exists(AUDIO_PATH):
        return
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_PATH)
    pygame.mixer.music.play()


def draw_progress_bar(current, total, width=50):
    progress = current / total
    filled = int(progress * width)
    bar = "█" * filled + "░" * (width - filled)
    percent = f"{progress * 100:5.1f}%"
    print(f"\033[0m[{bar}] {percent}\n", end="")


def player(frames, fps):
    global is_paused, current_frame
    total_frames = len(frames)
    frame_delay = 1 / fps if fps > 0 else 1 / 15
    start_time = time.time()

    threading.Thread(target=play_audio, daemon=True).start()

    while current_frame < total_frames:
        if keyboard.is_pressed('space'):
            is_paused = not is_paused
            if is_paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            time.sleep(0.3)

        if keyboard.is_pressed('left'):
            current_frame = max(0, current_frame - int(10 * fps))
            pygame.mixer.music.set_pos(current_frame / fps)
            start_time = time.time() - current_frame / fps
            time.sleep(0.3)

        if keyboard.is_pressed('right'):
            current_frame = min(total_frames - 1, current_frame + int(10 * fps))
            pygame.mixer.music.set_pos(current_frame / fps)
            start_time = time.time() - current_frame / fps
            time.sleep(0.3)

        if not is_paused:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')

            sys.stdout.write(frames[current_frame])
            sys.stdout.write("\n")
            draw_progress_bar(current_frame, total_frames)
            sys.stdout.flush()

            target_time = start_time + current_frame * frame_delay
            sleep_time = target_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

            current_frame += 1
        else:
            time.sleep(0.05)

    pygame.mixer.music.stop()
    pygame.mixer.quit()


def main():
    frames = load_preprocessed_frames(VIDEO_PATH)
    if frames is None:
        frames = preprocess_video(VIDEO_PATH, width=100)
        save_preprocessed_frames(frames, VIDEO_PATH)

    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    player(frames, fps)


if __name__ == "__main__":
    main()
