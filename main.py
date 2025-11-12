from pico2d import*
import random

current_stage =1

open_canvas()
background= load_image('map1.png')
character = load_image('Idle.png')
run_character = load_image('Run.png')

def handle_events():
    global running, dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir +=1
            elif event.key == SDLK_LEFT:
                dir -=1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -=1
            elif event.key == SDLK_LEFT:
                dir +=1


class monster:
    def __init__(self):
        self.x, self.y = random.randint(100,700), 90
        self.frame = random.randint(0,9)
        self.image = load_image('monster1.png')

    def update(self):
        self.frame = (self.frame + 1) % 10
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

monsters = [Monster() for i in range(5)]

running = True
x= 800//2
frame = 0
dir = 0

while running:
    handle_events()
    x += dir * 5
    x = max(0, min(x, 800))

    for monster in monsters:
        monster.update()
    clear_canvas()
    background.draw(400,300,800,600)
    for monster in monsters:
        monster.draw()

    if dir>0:
        run_character.clip_draw(frame*10,0,100,100,x,90)
        frame =(frame+1) % 8
    elif dir<0:
        run_character.clip_composite_draw(frame*10,0,100,100,0,'h',x,90,100,100)
        frame = (frame + 1) % 8
    else:
        character.clip_draw(frame*10,0,70,100,x,90)
        frame = (frame + 1) % 5

    update_canvas()
    delay(0.07)

close_canvas()

