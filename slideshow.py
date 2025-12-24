"""
Command to run in terminal (ctrl + shift + C) -> (ctrl + shift + V):
python3 /home/kunstcontact/Documents/Slideshow/slideshow.py
"""

import pygame
import os
import sys
import RPi.GPIO as GPIO
import time
import subprocess

# Configuration
STAGE_COUNT = 4
ARTWORKS_PER_STAGE = 3
IMAGE_FOLDER = "/home/kunstcontact/Documents/Resources/image"  # Root image directory, e.g. images/stage1/
VIDEO_FOLDER = "/home/kunstcontact/Documents/Resources/video"
current_stage = 0
current_index = 0
current_page = 0
showing_start = True
showing_title = False
showing_blank = False
play_audio = False
showing_artwork = False
showing_options = False
showing_selection = False
loading_screen_video = False
showing_video = False
running = True

# Init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

GPIO.setmode(GPIO.BCM)

NEXT_PIN = 5
BACK_PIN = 6
ARTWORK_PIN = [
    [1,7,8],
    [11,9,10],
    [22,27,17],
    [18,15,14]]
    
GPIO.setup(NEXT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for stage_pins in ARTWORK_PIN:
    for pin in stage_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
DEBOUNCE_MS = 300


# Load all images
def load_images():
    stages = []
    for stage_num in range(1, STAGE_COUNT + 1):
        path = os.path.join(IMAGE_FOLDER, f"stage{stage_num}")
        valid_exts = ('.jpg','.jpeg','.png')
        images = [
        pygame.image.load(os.path.join(path, img)).convert() 
        for img in sorted(os.listdir(path))
        if img.lower().endswith(valid_exts)]
        stages.append(images[:ARTWORKS_PER_STAGE])
    return stages
    
def load_image_individual():
    stage_images = []
    for stage_num in range(1, STAGE_COUNT + 1):
        folder = os.path.join(IMAGE_FOLDER, f"stage{stage_num}")
        images = sorted([
            os.path.join(folder,f) 
            for f in os.listdir(folder)
            if f.lower().endswith(('.jpg','.jpeg','.png'))
        ])
        stage_images.append(images)
    return stage_images
    
    
#scale images
def scale_image_to_fit(image, max_width, max_height):
    img_w, img_h = image.get_size()
    
    scale = min(max_width / img_w, max_height / img_h)
    new_size = (int(img_w * scale), int(img_h * scale))
    return pygame.transform.scale(image, new_size)
    

    
#GPIO buttons
def handle_next(channel):
    print ("Pressed Next")
    global showing_start, showing_title, showing_blank, play_audio, showing_artwork,showing_options, showing_selection, loading_screen_video, current_index, current_stage,current_page, running
    if current_page == 0:        #kmskb logo
        showing_start = False
        showing_title = True
        showing_blank = False
        showing_artwork = False
        current_index = 0
        current_stage = 0
        current_page += 1
        
    elif current_page == 1:      #titel phase 1
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 0
        current_stage = 0
        current_page += 1
    elif current_page == 2:      #blank page 1
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 0
        current_stage = 0
        current_page += 1
    elif current_page == 3:      #artwork 1
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 1
        current_stage = 0
        current_page += 1
    elif current_page == 4:      #blank page 2
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 1
        current_stage = 0
        current_page += 1
    elif current_page == 5:      #artwork 2
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 2
        current_stage = 0
        current_page += 1
    elif current_page == 6:      #blank page 3
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 2
        current_stage = 0
        current_page += 1
    elif current_page == 7:      #artwork 3
        showing_title = False
        showing_blank = False
        showing_artwork = False
        showing_options = True
        current_index = 0
        current_stage = 0
        current_page += 1
    elif current_page == 8:      #options phase 1
        showing_title = True
        showing_blank = False
        showing_artwork = False
        showing_options = False
        current_index = 0
        current_stage = 1
        current_page += 1
        
    elif current_page == 9:      #titel phase 2
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 0
        current_stage = 1
        current_page += 1
    elif current_page == 10:      #blank page 1
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 0
        current_stage = 1
        current_page += 1
    elif current_page == 11:      #artwork 1
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 1
        current_stage = 1
        current_page += 1
    elif current_page == 12:      #blank page 2
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 1
        current_stage = 1
        current_page += 1
    elif current_page == 13:      #artwork 2
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 2
        current_stage = 1
        current_page += 1
    elif current_page == 14:      #blank page 3
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 2
        current_stage = 1
        current_page += 1
    elif current_page == 15:      #artwork 3
        showing_title = False
        showing_blank = False
        showing_artwork = False
        showing_options = True
        current_index = 0
        current_stage = 1
        current_page += 1
    elif current_page == 16:      #options phase 2
        showing_title = True
        showing_blank = False
        showing_artwork = False
        showing_options = False
        current_index = 0
        current_stage = 2
        current_page += 1
    
    elif current_page == 17:      #titel phase 3
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 0
        current_stage = 2
        current_page += 1
    elif current_page == 18:      #blank page 1
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 0
        current_stage = 2
        current_page += 1
    elif current_page == 19:      #artwork 1
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 1
        current_stage = 2
        current_page += 1
    elif current_page == 20:      #blank page 2
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 1
        current_stage = 2
        current_page += 1
    elif current_page == 21:      #artwork 2
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 2
        current_stage = 2
        current_page += 1
    elif current_page == 22:      #blank page 3
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 2
        current_stage = 2
        current_page += 1
    elif current_page == 23:      #artwork 3
        showing_title = False
        showing_blank = False
        showing_artwork = False
        showing_options = True
        current_index = 0
        current_stage = 2
        current_page += 1
    elif current_page == 24:      #options phase 3
        showing_title = True
        showing_blank = False
        showing_artwork = False
        showing_options = False
        current_index = 0
        current_stage = 3
        current_page += 1
        
    elif current_page == 25:      #titel phase 4
        showing_title = False
        showing_blank = True
        play_audio = True
        showing_artwork = False
        current_index = 0
        current_stage = 3
        current_page += 1
    elif current_page == 26:      #blank page 1
        showing_title = False
        showing_blank = False
        play_audio = False
        pygame.mixer.music.stop()
        print("Stop Music")
        showing_artwork = True
        current_index = 0
        current_stage = 3
        current_page += 1
    elif current_page == 27:      #artwork 1
        showing_title = False
        showing_blank = True
        play_audio = True
        showing_artwork = False
        current_index = 1
        current_stage = 3
        current_page += 1
    elif current_page == 28:      #blank page 2
        showing_title = False
        showing_blank = False
        play_audio = False
        pygame.mixer.music.stop()
        print("Stop Music")
        showing_artwork = True
        current_index = 1
        current_stage = 3
        current_page += 1
    elif current_page == 29:      #artwork 2
        showing_title = False
        showing_blank = True
        play_audio = True
        showing_artwork = False
        current_index = 2
        current_stage = 3
        current_page += 1
    elif current_page == 30:      #blank page 3
        showing_title = False
        showing_blank = False
        play_audio = False
        pygame.mixer.music.stop()
        print("Stop Music")
        showing_artwork = True
        current_index = 2
        current_stage = 3
        current_page += 1
    elif current_page == 31:      #artwork 3
        showing_title = False
        showing_blank = False
        showing_artwork = False
        showing_options = True
        current_index = 0
        current_stage = 3
        current_page += 1
    elif current_page == 32:      #options phase 4
        showing_title = True
        showing_blank = False
        showing_artwork = False
        showing_options = False
        current_index = 0
        current_stage = 4
        current_page += 1
        
        
    elif current_page == 33:      #title selection
        showing_title = False
        showing_blank = False
        showing_artwork = False
        showing_selection = True
        loading_screen_video = False
        current_index = 0
        current_stage = 4
        current_page += 1 
    elif current_page == 34:      #selection
        showing_title = False
        showing_blank = False
        showing_artwork = False
        showing_selection = False
        loading_screen_video = True
        current_index = 0
        current_stage = 4
        current_page += 1 
    elif current_page == 35:      #video
        showing_title = False
        showing_blank = False
        showing_artwork = False
        showing_selection = False
        loading_screen_video = False
        current_index = 0
        current_stage = 4
        current_page += 1
        
    else:
        print("Reached end of slideshow")
    
    
    
    
            
def handle_back(channel):
    print ("Pressed Back")
    global showing_start, showing_title, showing_blank, showing_artwork, showing_options, showing_selection, loading_screen_video, current_index, current_stage,current_page, running
    
    #nothing happens on kmskb logo screen
        
    if current_page == 1:      #titel phase 1
        showing_start = True
        showing_title = False
        showing_blank = False
        showing_artwork = False
        current_index = 0
        current_stage = 0
        current_page -= 1
    elif current_page == 2:      #blank page 1
        showing_title = True
        showing_blank = False
        showing_artwork = False
        current_index = 0
        current_stage = 0
        current_page -= 1
    elif current_page == 3:      #artwork 1
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 1
        current_stage = 0
        current_page -= 1
    elif current_page == 4:      #blank page 2
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 1
        current_stage = 0
        current_page -= 1
    elif current_page == 5:      #artwork 2
        showing_title = False
        showing_blank = True
        showing_artwork = False
        current_index = 2
        current_stage = 0
        current_page -= 1
    elif current_page == 6:      #blank page 3
        showing_title = False
        showing_blank = False
        showing_artwork = True
        current_index = 2
        current_stage = 0
        current_page -= 1
    elif current_page == 7:      #artwork 3
        showing_title = True
        showing_blank = False
        showing_artwork = False
        current_index = 0
        current_stage = 1
        current_page += 1
                            
GPIO.add_event_detect(NEXT_PIN, GPIO.RISING, callback=handle_next, bouncetime=DEBOUNCE_MS) 
#GPIO.add_event_detect(BACK_PIN, GPIO.RISING, callback=handle_back, bouncetime=DEBOUNCE_MS)  

def play_audio_on_blank(artwork_index):
    
    audio_file = f"/home/kunstcontact/Documents/Resources/audio/{artwork_index + 1}.mp3"  
    print (f"Playing {audio_file}")
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()         
    
def show_options(stage, stage_images, screen):
    screen.fill((0,0,0))
    screen_rect = screen.get_rect()
    num_images = 3
    
    margin = 20
    available_width = screen_rect.width - (margin * (num_images + 1))
    image_width = available_width // num_images
    image_height = screen_rect.height - 2 * margin
    
    for i in range(num_images):
        
        img_path = stage_images[stage][i]
        #print (img_path)
        image = pygame.image.load(img_path).convert_alpha()
        
        orig_rect = image.get_rect()
        scale = min(image_width / orig_rect.width, image_height / orig_rect.height)
        new_size = (int(orig_rect.width * scale), int(orig_rect.height * scale))
        image = pygame. transform.smoothscale(image, new_size)
        
        x = margin + i * (image_width + margin)
        y = (screen_rect.height - new_size[1]) // 2
        
        screen.blit(image, (x,y))
    pygame.display.flip()    

def check_selection():
    selections = []
    for stage_index, stage_pins in enumerate(ARTWORK_PIN):
        selected_index = None
        for i, pin in enumerate(stage_pins):
            value = GPIO.input(pin)
            #print(f"Stage {stage_index + 1} Artwork{i}: GPIO {pin} = {value}")
            if GPIO.input(pin) == GPIO.HIGH:
                selected_index = i
                break
        if selected_index is None:
            #print(f"No selection for stage {stage_index + 1}")
            selections.append(-1)
        else:
            #print(f"Stage {stage_index +1} selected artwork: {selected_index}")
            selections.append(selected_index)
    return selections
        
def show_final_collage(selections, stage_images, screen):
    screen.fill((0,0,0))
    screen_rect = screen.get_rect()
    num_images = 4
    
    margin = 20
    available_width = screen_rect.width - (margin * (num_images + 1))
    image_width = available_width // num_images
    image_height = screen_rect.height - 2 * margin
    
    for i, selected_index in enumerate(selections):
        if selected_index == -1:
            continue
            
        img_path = stage_images[i][selected_index]
        #print (img_path)
        image = pygame.image.load(img_path).convert_alpha()
        
        orig_rect = image.get_rect()
        scale = min(image_width / orig_rect.width, image_height / orig_rect.height)
        new_size = (int(orig_rect.width * scale), int(orig_rect.height * scale))
        image = pygame. transform.smoothscale(image, new_size)
        
        x = margin + i * (image_width + margin)
        y = (screen_rect.height - new_size[1]) // 2
        
        screen.blit(image, (x,y))
    pygame.display.flip()

            
def make_final_video(selections, stage_images):
    video_base = VIDEO_FOLDER
    audio_file = f"/home/kunstcontact/Documents/Resources/audio/{selections[3] + 1}.mp3"
    filelist_name = "filelist.txt"
    target_w, target_h = width, height
    
    video_paths = []
    for stage_num, selected_index in enumerate(selections):
        if selected_index == -1:
            continue
        img_path = stage_images[stage_num][selected_index]
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        video_path = os.path.join(video_base, f"stage{stage_num+1}",f"{base_name}.mp4")
        if os.path.exists(video_path):
            video_paths.append(video_path)
        else:
            print(f"Video not found for:{video_path}")
        
    if not video_paths:
        print("No videos to combine")
        return
        
    with open(filelist_name, 'w') as f:
        for path in video_paths:    
            f.write(f"file '{os.path.abspath(path)}'\n")
    

           
    
    subprocess.run([
    'ffmpeg','-y',
    '-f', 'concat',
    '-safe', '0',
    '-i', filelist_name,
    '-c','copy',
    'combined_once.mp4'
    ])
    subprocess.run([
    'ffmpeg','-y',
    '-stream_loop', '4',
    '-i', 'combined_once.mp4',
    '-c','copy',
    'combined_multiple.mp4'
    ])
    subprocess.run([
    'ffmpeg','-y',
    '-i', 'combined_multiple.mp4',
    '-i', audio_file,
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-shortest',
    'final_with_audio.mp4'
    ])
    print("Playing final combined video in loop")
    

        
# Main loop
def main():
    global showing_start, showing_title, showing_blank, play_audio, showing_artwork, showing_options, showing_selection, loading_screen_video, showing_video, current_index, current_stage,current_page, running
    stages = load_images()
    stages_ind = load_image_individual()
    
    stage_titles = ["Wie / Qui","Waar / Ou","Met wie / Avec qui","Wat / Quoi","Gekozen verhaal / Histoire choisie"]
    blank_instructions = [ 
    ["Kunstwerk/Art 1","Kunstwerk/Art 2","Kunstwerk/Art 3"],
    ["Geur/Odeur 1","Geur/Odeur 2","Geur/Odeur 3"],
    ["Object/Objet 1","Object/Objet 2","Object/Objet 3"],
    ["Lied/Chanson 1","Lied/Chanson 2","Lied/Chanson 3"]] 


    while running:
        screen.fill((0, 0, 0))
        if showing_start:
            logo_img = pygame.image.load("/home/kunstcontact/Documents/Resources/image/Z_Front_page/MuséeRoyalMuseums_logo2lines2.jpg").convert_alpha()
            scaled_logo_img = scale_image_to_fit(logo_img, width*0.8, height*0.8)
            rect = scaled_logo_img.get_rect(center=(width//2, height//2))
            screen.blit(scaled_logo_img, rect)
        
        elif showing_title:
            font = pygame.font.SysFont(None, 100)
            title_text = stage_titles[current_stage] if current_stage < len(stage_titles) else f"Stage {current_stage + 1}"
            text = font.render(title_text,True,(255,255,255))
            text_rect = text.get_rect(center=(width //2, height//2))
            screen.blit(text, text_rect)
            
        elif showing_blank:
            instruction_text = blank_instructions[current_stage][current_index]
            font = pygame.font.SysFont(None, 60)
            info_text = font.render(instruction_text,True,(180,180,180))
            info_rect = text.get_rect(center=(width //2, height - 80))
            screen.blit(info_text, info_rect)
            if play_audio:
                play_audio_on_blank(current_index)
                play_audio = False
            
        elif showing_artwork:
            image = stages[current_stage][current_index]
            scaled_img = scale_image_to_fit(image, width *0.95, height *0.95)
            img_rect = scaled_img.get_rect(center=(width // 2, height // 2))
            screen.blit(scaled_img, img_rect)
            
        elif showing_options:
            show_options(current_stage, stages_ind, screen)
            
        elif showing_selection:
            selection = check_selection()
            #print (selection)
            show_final_collage(selection, stages_ind, screen)
        
        elif loading_screen_video:
            font = pygame.font.SysFont(None, 60)
            text = font.render("Even geduld/Patience",True,(180,180,180))
            text_rect = text.get_rect(center=(width //2, height - 80))
            screen.blit(text, text_rect)
            showing_video = True
            running = False
            
        """elif showing_video:    
            make_final_video(selection, stages_ind)
            showing_video = False
            exit_making_video = True"""
        

            
        pygame.display.flip()
        clock.tick(30)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                GPIO.cleanup()  
                pygame.quit()
                sys.exit()
    
    
    

if __name__ == "__main__":
    
    main()
    
    stages_ind = load_image_individual()
    selection = check_selection()
    make_final_video(selection, stages_ind)
    
    GPIO.cleanup()                
    pygame.quit()
    subprocess.run(['vlc','--fullscreen','--play-and-exit','final_with_audio.mp4'])
    
