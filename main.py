from pico2d import*

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

running = True
x= 800//2
frame = 0
dir = 0
while running:
    clear_canvas()
    background.draw(400,300,800,600)

    if dir>0:
        run_character.clip_draw(frame*20,0,100,100,x,90)
    elif dir<0:
        run_character.clip_composite_draw(frame*70,0,100,100,0,'h',x,90,100,100)
    else:
        character.clip_draw(frame*60,0,100,100,x,90)
    update_canvas()
    handle_events()
    frame =(frame+1)%5
    x += dir *5
    x=max(0,min(x,800))
    delay(0.1)

close_canvas()

