# dividir_audio.py

import moviepy.editor as mp
from pydub import AudioSegment
from pydub.utils import which
import os
from tkinter import Tk, filedialog

# Configurar o ffmpeg para pydub
AudioSegment.converter = which("ffmpeg")

def select_file():
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    file_path = filedialog.askopenfilename(
        title="Selecione o vídeo MP4 ou áudio MP3",
        filetypes=[("Arquivos de vídeo e áudio", "*.mp4;*.mp3")]
    )
    return file_path

def extract_audio_from_video(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def split_audio(audio_path, output_dir, output_format):
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio)
    part_duration = duration // 5

    for i in range(5):
        start_time = i * part_duration
        end_time = (i + 1) * part_duration if i < 4 else duration  # Ensure the last part gets the remainder
        part_audio = audio[start_time:end_time]
        part_audio.export(os.path.join(output_dir, f"part_{i + 1}.{output_format}"), format=output_format)

if __name__ == "__main__":
    print("Bem-vindo ao divisor de áudio.")
    file_path = select_file()
    if not file_path:
        print("Nenhum arquivo selecionado.")
    elif not os.path.exists(file_path):
        print(f"O caminho fornecido não existe: {file_path}")
    else:
        output_dir = "audio_parts"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            if file_path.endswith(".mp4"):
                audio_path = "extracted_audio.wav"
                print("Extraindo áudio do vídeo...")
                extract_audio_from_video(file_path, audio_path)
                print("Áudio extraído com sucesso.")
                print("Dividindo áudio em 5 partes...")
                split_audio(audio_path, output_dir, output_format="wav")
                os.remove(audio_path)
            elif file_path.endswith(".mp3"):
                audio_path = file_path
                print("Dividindo áudio em 5 partes...")
                split_audio(audio_path, output_dir, output_format="mp3")
            print(f"Áudio dividido com sucesso. As partes estão salvas na pasta '{output_dir}'.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
