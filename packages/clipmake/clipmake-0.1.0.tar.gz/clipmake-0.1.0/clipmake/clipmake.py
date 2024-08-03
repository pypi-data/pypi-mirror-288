import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def random_segments(video_path, output_duration=60, num_segments=5):
    video_clip = VideoFileClip(video_path)
    duration_per_segment = output_duration / num_segments
    segments = []

    for _ in range(num_segments):
        start_time = random.uniform(0, video_clip.duration - duration_per_segment)
        end_time = start_time + duration_per_segment
        segment = video_clip.subclip(start_time, end_time)
        segments.append(segment)

    final_clip = concatenate_videoclips(segments)
    return final_clip

def main():
    language = input("Choose your language / Выберите язык (E/R): ").strip().lower()
    if language == 'r':
        lang = 'ru'
    elif language == 'e':
        lang = 'en'
    else:
        print("Invalid choice / Неверный выбор")
        return

    while True:
        if lang == 'ru':
            print("Сделано Avinion")
            print("Telegram: @akrim")

            input_path = input("Введите путь к входному видеофайлу: ")
            output_path = input("Введите путь для сохранения выходного видеофайла: ")
            output_duration = int(input("Введите желаемую длительность выходного видео (в секундах): "))
            num_segments = int(input("Введите количество сегментов для склеивания: "))

            final_clip = random_segments(input_path, output_duration, num_segments)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp.m4a", remove_temp=True, fps=24, preset="ultrafast", ffmpeg_params=["-strict", "experimental"])

            continue_choice = input("Хотите продолжить? (Y/N): ").strip().lower()
        else:
            print("Made By Avinion")
            print("Telegram: @akrim")

            input_path = input("Enter the path to the input video file: ")
            output_path = input("Enter the path to save the output video file: ")
            output_duration = int(input("Enter the desired output video duration (in seconds): "))
            num_segments = int(input("Enter the number of segments to concatenate: "))

            final_clip = random_segments(input_path, output_duration, num_segments)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp.m4a", remove_temp=True, fps=24, preset="ultrafast", ffmpeg_params=["-strict", "experimental"])

            continue_choice = input("Do you want to continue? (Y/N): ").strip().lower()

        if continue_choice == 'n':
            break
        else:
            clear_console()

if __name__ == "__main__":
    main()
