# This file will look for new folder in user_upload and generate reels if they are not already in done folder
import os
from text_to_speech import text_to_speech_file
import time
import subprocess

def text_to_audio(folder):
    with open(f"user_upload/{folder}/desc.txt", "r") as f:
        text = f.read()
    print(text , folder)
    text_to_speech_file(text , folder)

def create_reels(folder):
    # command = f'''ffmpeg -f concat -safe 0 -i user_upload/{folder}/input.txt -i user_upload/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
    command = f'''ffmpeg -f concat -safe 0 -i user_upload/{folder}/input.txt -i user_upload/{folder}/audio.mp3 -map 0:v:0 -map 1:a:0 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -c:a aac -ar 44100 -shortest -r 30 -pix_fmt yuv420p -y static/reels/{folder}.mp4'''
    subprocess.run(command,shell=True,check=True)

    
if __name__ == "__main__" :
    
    while True:
        print("Running que....")
    # reads the content inside of done.txt folder and store it to done_folder
        with open("done.txt","r") as f : 
            done_folder = f.readlines()
        
    # strip i.e deleted the extra spaces from done_folder
        done_folder = [f.strip() for f in done_folder] 
        
    # assign the list of names of user_upload folder to var(folders)
        folders = os.listdir("user_upload")
        
    # This function runs (text_to_audio,create_reels) methods from each new folder in user upload folder and save the name of folder after performing operations to done folder the folder that already exist does not goes through creation again
        for folder in folders : 
            if (folder not in done_folder):
                text_to_audio(folder)
                create_reels(folder)
                with open("done.txt","a") as f:
                    f.write(folder + "\n")
    
    
        time.sleep(4)    
        
            
            
                