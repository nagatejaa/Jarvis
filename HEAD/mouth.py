# import asyncio
# import threading
# import os
# import edge_tts
# import pygame
#
# VOICE = "en-AU-WilliamNeural"
# BUFFER_SIZE = 1024
#
#
# def remove_file(file_path):
#     max_attempts = 3
#     attempts = 0
#     while attempts < max_attempts:
#         try:
#             os.remove(file_path)
#             print(f"Successfully removed {file_path}")
#             break
#         except Exception as e:
#             print(f"Error removing file: {e}")
#             attempts += 1
#
#
# async def amain(TEXT, output_file) -> None:
#     try:
#         cm_txt = edge_tts.Communicate(TEXT, VOICE)
#         await cm_txt.save(output_file)
#         print(f"Saved speech to {output_file}")
#
#         # Start a new thread for playing audio
#         thread = threading.Thread(target=play_audio, args=(output_file,))
#         thread.start()
#         thread.join()  # Ensure that the audio is fully played before removing the file
#
#     except Exception as e:
#         print(f"Error during speech synthesis: {e}")
#     finally:
#         remove_file(output_file)
#
#
# def play_audio(file_path):
#     try:
#         pygame.init()
#         pygame.mixer.init()
#         sound = pygame.mixer.Sound(file_path)
#         sound.play()
#
#         # Wait until the sound finishes playing
#         while pygame.mixer.get_busy():
#             pygame.time.Clock().tick(10)
#
#     except Exception as e:
#         print(f"Error playing audio: {e}")
#     finally:
#         pygame.quit()  # Ensure pygame is properly quit after playing
#
#
# def speak(TEXT, output_file=None):
#     if output_file is None:
#         output_file = f"{os.getcwd()}/speak.mp3"
#     asyncio.run(amain(TEXT, output_file))
#
#
# speak("Welcome to the world of Jarvis")


# mouth.py

import asyncio
import threading
import os
import edge_tts
import pygame

VOICE = "en-AU-WilliamNeural"
BUFFER_SIZE = 1024

def remove_file(file_path):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            os.remove(file_path)
            break
        except Exception as e:
            print(f"Error removing file: {e}")
            attempts += 1

async def amain(TEXT, output_file) -> None:
    try:
        cm_txt = edge_tts.Communicate(TEXT, VOICE)
        await cm_txt.save(output_file)


        # Start a new thread for playing audio
        thread = threading.Thread(target=play_audio, args=(output_file,))
        thread.start()
        thread.join()  # Ensure that the audio is fully played before removing the file

    except Exception as e:
        print(f"Error during speech synthesis: {e}")
    finally:
        remove_file(output_file)

def play_audio(file_path):
    try:
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()

        # Wait until the sound finishes playing
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        pygame.quit()  # Ensure pygame is properly quit after playing

def speak(TEXT, output_file=None):
    if output_file is None:
        output_file = f"{os.getcwd()}/speak.mp3"
    asyncio.run(amain(TEXT, output_file))


speak("hello")