from pico2d import*
import random
import math
class BehaviorTree:
    def __init__(self,root):
        self.root = root
        self.tick_counter = 0

    def run(self):
        self.tick_counter +=1
        return self.root.run()

class Action:
    def __init__(self,name,action_func,*args):
        self.name = name
        self.action_func = action_func
        self.args = args
    def run(self):
        return self.action_func(*self.args)

class Condition:
    def __init__(self,name,condition_func,*args):
        self.name = name
        self.condition_func = condition_func
        self.args = args

    def run(self):
        if self.condition_func(*self.args):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAILURE

class Composite:
    def __init__(self,name,*children):
        self.name = name
        self.children = children

class Sequence(Composite):
    def run(self):
        for child in self.children:
            status = child.run()
            if status != BehaviorTree.SUCCESS:
                return status
        return BehaviorTree.SUCCESS

class Selector(Composite):
    def run(self):
        for child in self.children:
            status = child.run()
            if status != BehaviorTree.FAILURE:
                return status
        return BehaviorTree.FAILURE

BehaviorTree.SUCCESS =1
BehaviorTree.FAILURE =2
BehaviorTree.RUNNING =3

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

MONSTER_DETECTION_RANGE = 200
MONSTER_SPEED = 2
AI_UPDATE_INTERVAL = 0.1

open_canvas()
background= load_image('map1.png')
character = load_image('Idle.png')
run_character = load_image('Run.png')
attack_character = load_image('Attack_1.png')
key_image=load_image('key.png')
attack2_character= load_image('Attack_2.png')
background2= load_image('map2.png')
monster2_image= load_image('monster2.png')
background3= load_image('map3.png')
monster3_image= load_image('bossmonster.png')
attack_state=False
attack_frame=0
key_attack_state=False
key_attack_frame=0
face_dir=1
collision=20
player_hp=3
MONSTER_KILL_TIME=1.0
KEY_KILL_TIME=1.0
PLAYER_KILL_TIME=2.0

def get_boy_bb(cx,cy):
    return cx - 30, cy - 40, cx + 30, cy + 40
def get_boy_pos():
    global x,y
    return x,y


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
        self.kill_start_time=None
    def draw(self):
        key_image.draw(self.x,self.y,50,50)

    def get_bb(self):
        return self.x-self.bb_width/2,self.y-self.bb_height/2,self.x+self.bb_width/2,self.y+self.bb_height/2



class monster:
    def __init__(self):
        self.x, self.y = random.randint(10,700),random.randint(0,500)
        self.frame = random.randint(0,5)
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
        self.x, self.y = random.randint(10, 700), random.randint(0, 500)
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

class monster3:
    def __init__(self):
        self.x,self.y=400,300
        self.frame = random.randint(0,7)
        self.image= monster3_image
        self.collision_frame=0
        self.width =250
        self.height =250
        self.bb_width=70
        self.bb_height=70
        self.collision_start_time=None
        self.kill_start_time=None

        self.target_x,self.target_y= self.x,self.y
        self.dir_x=0
        self.dir_y=0
        self.is_moving=False
        self.last_ai_update_time= get_time()
        self.build_behavior_tree()

    def build_behavior_tree(self):
        a_set_random = Action('랜덤위치설정',self.set_random_location)
        a_move_to_target = Action('목표위치이동',self.move_to)
        a_move_to_boy= Action('소년추적위치설정',self.set_target_location,get_boy_pos)
        c_boy_nearby= Condition('소년근처에있는가?',self.if_boy_nearby,MONSTER_DETECTION_RANGE)
        wander = Sequence('배회행동',a_set_random,a_move_to_target)
        chase_boy= Sequence('소년추적행동',c_boy_nearby,a_move_to_boy,a_move_to_target)
        chase_or_wander = Selector('소년이 가까이있으면 추적하고 아니면 배회',chase_boy,wander)
        self.bt= BehaviorTree(chase_or_wander)

    def if_boy_nearby(self,detection_range):
        boy_x,boy_y = get_boy_pos()
        distance = math.sqrt((self.x-boy_x)**2 + (self.y-boy_y)**2)
        return distance < detection_range

    def set_random_location(self):
        angle = random.uniform(0, 2*math.pi)
        distance = random.uniform(50,200)
        new_x = self.x + distance* math.cos(angle)
        new_y = self.y + distance* math.sin(angle)
        self.target_x = max(0, min(new_x,750))
        self.target_y = max(0, min(new_y,650))
        self.is_moving = True
        return BehaviorTree.SUCCESS

    def set_target_location(self,target_func):
        self.target_x, self.target_y = target_func()
        self.is_moving = True
        return BehaviorTree.SUCCESS

    def move_to(self):
        if not self.is_moving:
            return BehaviorTree.SUCCESS
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < MONSTER_SPEED:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False
            return BehaviorTree.SUCCESS
        self.dir_x = dx / distance
        self.dir_y = dy / distance
        self.x += self.dir_x * MONSTER_SPEED
        self.y += self.dir_y * MONSTER_SPEED
        return BehaviorTree.RUNNING

    def update(self):
        self.frame = (self.frame + 1) % 8
        current_time = get_time()
        if current_time - self.last_ai_update_time >= AI_UPDATE_INTERVAL:
            self.bt.run()
            self.last_ai_update_time = current_time
    def get_bb(self):
        return self.x - self.bb_width / 2, self.y - self.bb_height / 2, self.x + self.bb_width / 2, self.y + self.bb_height / 2
    def draw(self):
        left_x= self.frame * 80
        bottom_y=210
        clip_width=60
        clip_height=130
        if self.dir_x < 0:
            self.image.clip_composite_draw(left_x,bottom_y,clip_width,clip_height,0,'h',self.x,self.y,self.width,self.height)
        else:
            self.image.clip_draw(left_x,bottom_y,clip_width,clip_height,self.x,self.y,self.width,self.height)


monsters = [monster() for i in range(5)]
keys=[Key() for i in range(2)]



running = True
x= 800//2
frame = 0
dir = 0
y=90
dir_y=0

while running:
    handle_events()
    current_time = get_time()
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

    for key in keys:
        key_bb = key.get_bb()
        if key_attack_state and game_world.collide(boy_bb,key_bb):
            if key.kill_start_time is None:
                key.kill_start_time = current_time
            if current_time-key.kill_start_time >= KEY_KILL_TIME:
                keys_to_remove.append(key)
        else:
            key.kill_start_time = None

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

    if current_stage ==2 or current_stage==3:
        for m in monsters:
            if game_world.collide(boy_bb,m.get_bb()):
                if m.collision_start_time is None:
                    m.collision_start_time = current_time
                elif current_time - m.collision_start_time >= PLAYER_KILL_TIME:
                    player_hp -= 1
                    m.collision_start_time = None
                    if player_hp <= 0:
                        running = False
            else:
                if m.collision_start_time is not None:
                    m.collision_start_time = None

    monsters= [m for m in monsters if m not in monsters_to_remove]
    keys= [k for k in keys if k not in keys_to_remove]

    if not monsters and not keys:
        if current_stage==1:
            current_stage+=1
            background= background2
            monsters = [monster2() for i in range (5)]
            keys = [Key() for i in range(1)]
        elif current_stage==2:
            current_stage+=1
            background= background3
            monsters =[monster3()]
            keys =[]
    if current_stage==3 and not monster:
        running = False




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
