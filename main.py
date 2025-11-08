from pico2d import*

current_stage =1

open_canvas()
background= load_image('map1.png')

running = True
while running:
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


