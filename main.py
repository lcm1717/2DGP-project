from pico2d import*
import random

current_stage =1

open_canvas()
background= load_image('map1.png')
character = load_image('Idle.png')
run_character = load_image('Run.png')
attack_character = load_image('Attack_1.png')


def handle_events():
    global running, dir,dir_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir +=1
            elif event.key == SDLK_LEFT:
                dir -=1
            elif event.key == SDLK_UP:
                dir_y +=1
            elif event.key == SDLK_DOWN:
                dir_y -=1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -=1
            elif event.key == SDLK_LEFT:
                dir +=1
            elif event.key == SDLK_UP:
                dir_y -=1
            elif event.key == SDLK_DOWN:
                dir_y +=1


class monster:
    def __init__(self):
        self.x, self.y = random.randint(0,800),random.randint(0,600)
        self.frame = random.randint(0,4)
        self.image = load_image('monster1.png')

    def update(self):
        self.frame = (self.frame + 1) % 5


    def draw(self):
        self.image.clip_draw(self.frame * 45, 0, 45, 60, self.x, self.y,60,60)

monsters = [monster() for i in range(4)]

running = True
x= 800//2
frame = 0
dir = 0
y=90
dir_y=0

while running:
    handle_events()
    x += dir * 5
    y += dir_y *5
    x = max(0, min(x, 800))
    y = max(0, min(y, 600))

    for monster in monsters:
        monster.update()
    clear_canvas()
    background.draw(400,300,800,600)
    for monster in monsters:
        monster.draw()

    if dir>0:
        run_character.clip_draw(frame*130,0,130,80,x,y)
        frame =(frame+1) % 8
    elif dir<0:
        run_character.clip_composite_draw(frame*130,0,130,100,0,'h',x,y,100,100)
        frame = (frame + 1) % 8
    else:
        character.clip_draw(frame*130,0,130,100,x,y)
        frame = (frame + 1) % 2

    update_canvas()
    delay(0.1)

close_canvas()

