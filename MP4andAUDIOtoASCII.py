import pygame
import threading
import os
import time
import cv2

VIDEO_PATH = "video_file.mp4"
AUDIO_PATH = "audio_file.mp3"
ASCII_CHARS = "█▓▒░$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'."


def frame_to_ascii(frame, new_width=160):
    height, width, _ = frame.shape
    aspect_ratio = width / height
    new_height = int(new_width / aspect_ratio / 2.1)
    resized = cv2.resize(frame, (new_width, new_height))

    ascii_frame = ""
    for row in resized:
        for pixel in row:
            blue, green, red = pixel
            brightness = 0.2126 * red + 0.7152 * green + 0.0722 * blue
            char = ASCII_CHARS[int(brightness / 255 * (len(ASCII_CHARS) - 1))]
            ascii_frame += f"\033[38;2;{red};{green};{blue}m{char}\033[0m"
        ascii_frame += "\n"
    return ascii_frame


def play_audio():
    if os.path.exists(AUDIO_PATH):
        pygame.mixer.init()
        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play()


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: could not open video file.")
        return

    if os.path.exists(AUDIO_PATH):
        threading.Thread(target=play_audio, daemon=True).start()

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1 / fps if fps > 0 else 1 / 15

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ascii_frame = frame_to_ascii(frame, new_width=140)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_frame)
            time.sleep(frame_delay)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        pygame.mixer.quit()


if __name__ == "__main__":
    main()
