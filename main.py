from pico2d import*
import random
class GameWorld:
    def collide(self,a_bb,b_bb):
        left_a, bottom_a, right_a, top_a = a_bb
        left_b, bottom_b, right_b, top_b = b_bb

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True
game_world = GameWorld()
current_stage =1

open_canvas()
background= load_image('map1.png')
character = load_image('Idle.png')
run_character = load_image('Run.png')
attack_character = load_image('Attack_1.png')
key_image=load_image('key.png')
attack2_character= load_image('Attack_2.png')
background2= load_image('map2.png')
monster2_image= load_image('monster2.png')

attack_state=False
attack_frame=0
key_attack_state=False
key_attack_frame=0
face_dir=1
collision=20
player_hp=3
MONSTER_KILL_TIME=3.0
PLAYER_KILL_TIME=5.0

def get_boy_bb(cx,cy):
    return cx - 30, cy - 40, cx + 30, cy + 40


def handle_events():
    global running, dir,dir_y,face_dir,attack_state,key_attack_state, attack_frame, key_attack_frame

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir +=1
                face_dir=1
            elif event.key == SDLK_LEFT:
                dir -=1
                face_dir=-1
            elif event.key == SDLK_UP:
                dir_y +=1
            elif event.key == SDLK_DOWN:
                dir_y -=1
            elif event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_a:
                attack_state = True
                key_attack_state = False
                key_attack_frame = 0
            elif event.key == SDLK_s:
                key_attack_state = True
                attack_state = False
                attack_frame = 0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -=1
            elif event.key == SDLK_LEFT:
                dir +=1
            elif event.key == SDLK_UP:
                dir_y -=1
            elif event.key == SDLK_DOWN:
                dir_y +=1
            elif event.key == SDLK_a:
                attack_state = False
                attack_frame = 0
            elif event.key == SDLK_s:
                key_attack_state = False
                key_attack_frame = 0


class Key:
    def __init__(self):
        self.x,self.y= random.randint(100,750),random.randint(100,550)
        self.image= load_image('key.png')
        self.bb_width=30
        self.bb_height=30
        self.collided=False
        self.collision_time=0
    def draw(self):
        key_image.draw(self.x,self.y,50,50)


    def get_bb(self):
        return self.x-self.bb_width/2,self.y-self.bb_height/2,self.x+self.bb_width/2,self.y+self.bb_height/2



class monster:
    def __init__(self):
        self.x, self.y = random.randint(0,700),random.randint(0,500)
        self.frame = random.randint(0,4)
        self.image = load_image('monster1.png')
        self.collision_frame=0
        self.width =60
        self.height =60
        self.bb_width=20
        self.bb_height=20
        self.kill_start_time=None

    def update(self):
        self.frame = (self.frame + 1) % 5

    def get_bb(self):
        return self.x-self.bb_width/2,self.y-self.bb_height/2,self.x+self.bb_width/2,self.y+self.bb_height/2

    def draw(self):
        self.image.clip_draw(self.frame*45,0,45,60,self.x,self.y,self.width,self.height)

class monster2:
    def __init__(self):
        self.x, self.y = random.randint(0, 700), random.randint(0, 500)
        self.frame = random.randint(0, 3)
        self.image = monster2_image
        self.collision_frame = 0
        self.width = 60
        self.height = 60
        self.bb_width = 20
        self.bb_height = 20
        self.collision_start_time = None
        self.kill_start_time=None
    def update(self):
        self.frame = (self.frame + 1) % 4

    def get_bb(self):
        return self.x-self.bb_width/2,self.y-self.bb_height/2,self.x+self.bb_width/2,self.y+self.bb_height/2

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 36, 45, self.x, self.y, self.width, self.height)



monsters = [monster() for i in range(4)]
keys=[Key() for i in range(2)]

running = True
x= 800//2
frame = 0
dir = 0
y=90
dir_y=0

while running:
    handle_events()
    if not attack_state and not key_attack_state:
        x += dir * 5
        y += dir_y *5
        x = max(0, min(x, 800))
        y = max(0, min(y, 600))

    for m in monsters:
        m.update()
    boy_bb=get_boy_bb(x,y)
    monsters_to_remove=[]
    keys_to_remove=[]
    current_time = get_time()
    for key in keys:
        key_bb = key.get_bb()
        if key_attack_state and key.collided == False and game_world.collide(boy_bb,key_bb):
            key.collided=True
            key.collision_time=get_time()
        if key.collided and get_time()-key.collision_time>=1.5:
            keys_to_remove.append(key)

        if attack_state:
            for m in monsters:
                monster_bb = m.get_bb()
                if game_world.collide(boy_bb,monster_bb):
                    if m.kill_start_time is None:
                        m.kill_start_time = current_time
                    if current_time-m.kill_start_time >=MONSTER_KILL_TIME:
                        monsters_to_remove.append(m)
                else:
                    m.kill_start_time = None
        else:
            for m in monsters:
                m.kill_start_time = None
    if current_stage ==2:
        global player_hp
        for m in monsters:
            if game_world.collide(boy_bb,m.get_bb()):
                if m.collision_start_time is None:
                    m.collision_start_time = current_time
                elif current_time - m.collision_start_time >= PLAYER_KILL_TIME:
                    player_hp -= 1
                    m.collision_start_time = None
                    if player_hp <= 0:
                        running = False

        if attack_state:
            for m in monsters:
                monster_bb = m.get_bb()
                if game_world.collide(boy_bb,m.get_bb()):
                    m.hit_count+=1
                    if m.collision_frame >= collision:
                        monsters_to_remove.append(m)
                else:
                    m.collision_frame=0
        else:
            for m in monsters:
                m.collision_frame=0

        for m in monster:
            if game_world.collide(boy_bb,m.get_bb()):
                current_time = get_time()
                if m.collision_start_time is None:
                    m.collision_start_time = current_time
                elif current_time-m.collision_start_time>=5.0:
                    player_hp -=1
                    m.collision_start_time = None
                    if player_hp <= 0:
                        running = False
        else:
            if m.collision_start_time is not None:
                m.collision_start_time = None

    monsters= [m for m in monsters if m not in monsters_to_remove]
    keys= [k for k in keys if k not in keys_to_remove]

    if not monsters and not keys and current_stage==1:
        current_stage+=1
        background= background2
        monsters = [monster2() for i in range (5)]
        keys = [Key() for i in range(1)]
    clear_canvas()
    background.draw(400,300,800,600)



    for m in monsters:
        m.draw()
    for key in keys:
        key.draw()

    if attack_state:
        if face_dir ==1:
            attack_character.clip_draw(attack_frame*130,0,130,100,x,y)
        else:
            attack_character.clip_composite_draw(attack_frame*130,0,130,100,0,'h',x,y,100,100)
        attack_frame= (attack_frame + 1) % 6
    elif key_attack_state:
        if face_dir ==1:
            attack2_character.clip_draw(key_attack_frame*130,0,130,100,x,y)
        else:
            attack2_character.clip_composite_draw(key_attack_frame*130,0,130,100,0,'h',x,y,100,100)
        key_attack_frame= (key_attack_frame + 1) % 8
    else:
        if dir>0:
            run_character.clip_draw(frame*130,0,130,80,x,y)
            frame =(frame+1) % 8
        elif dir<0:
            run_character.clip_composite_draw(frame*130,0,130,100,0,'h',x,y,100,100)
            frame = (frame + 1) % 8
        else:
            if face_dir==1:
                character.clip_draw(frame*130,0,130,100,x,y)
            else:
                character.clip_composite_draw(frame*130,0,130,100,0,'h',x,y,100,100)
            frame = (frame + 1) % 2



    update_canvas()
    delay(0.03)

close_canvas()
