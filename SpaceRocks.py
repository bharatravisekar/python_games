# Author: Bharat Ravisekar
# Date: 06/15/2013

# program template for Spaceship
import simplegui
import math
import random

# configuration constants
WIDTH = 800
HEIGHT = 600
LINEAR_ACC = 0.22
ANGLE_VEL = 0.08
FRICTION_DESC = 0.02
MISSILE_VEL = 4.5
MAX_LIVES = 3
MAX_ROCKS = 10

# global variables
score = 0
lives = MAX_LIVES
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris_blend.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.vel[0] *= (1 - FRICTION_DESC)
        self.vel[1] *= (1 - FRICTION_DESC)            
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += LINEAR_ACC * forward[0]
            self.vel[1] += LINEAR_ACC * forward[1]
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        forward = angle_to_vector(self.angle)
        initial_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        initial_vel = [self.vel[0] + forward[0] * MISSILE_VEL, self.vel[1] + forward[1] * MISSILE_VEL]
        a_missile = Sprite(initial_pos, initial_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            image_index = math.floor(self.age) % self.lifespan
            image_pos =  [explosion_info.get_center()[0] + image_index * explosion_info.get_size()[0], explosion_info.get_center()[1]]
            canvas.draw_image(self.image, image_pos, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 0.6
        if self.age > self.lifespan:
            return True
        else:
            return False
                    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) < (self.radius + other_object.radius - 1):
            return True
        else:
            return False        
     
# key and mouse handlers
def keydown_handler(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = -ANGLE_VEL
    elif key == simplegui.KEY_MAP["right"]:    
        my_ship.angle_vel = ANGLE_VEL
    elif key == simplegui.KEY_MAP["space"]:    
        my_ship.shoot()
            
def keyup_handler(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["right"]:    
        my_ship.angle_vel = 0

def mouse_handler(position):
    if started == False:
        restart()
                
# main draw handler
def draw(canvas):
    global time, lives, score, started
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)    

    # update and draw the sprite groups
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # update ship and sprites
    my_ship.update()
    
    # check ship and rock collision
    collisions = group_collide(rock_group, my_ship)
    if collisions > 0:
        lives -= 1
    
    if lives <= 0:
        stop()
    
    # check missile-rock collision
    missile_rock_collisions = group_group_collide(rock_group, missile_group)
    score += missile_rock_collisions
        
    # lives and score
    canvas.draw_text("Lives", [50, 50], 18, "Yellow", "monospace")
    canvas.draw_text(str(lives), [70, 70], 18, "Yellow", "monospace")
    canvas.draw_text("Score", [WIDTH - 100, 50], 18, "Yellow", "monospace")
    canvas.draw_text(str(score), [WIDTH - 80, 70], 18, "Yellow", "monospace")
    
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
      
# utility methods
def restart():
    global lives, score, started
    lives = MAX_LIVES
    score = 0
    started = True

def stop():
    global started, missile_group, rock_group, explosion_group
    missile_group = set([])
    rock_group = set([])    
    explosion_group = set([])
    started = False
    
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group    
    if len(rock_group) < 12 and started == True:
        random_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        random_velocity = [(random.randrange(0, 20) - 10) / 10, (random.randrange(0, 20) - 10) / 10]
        random_ang_vel = (random.randrange(0, 20) - 10) / 100
        a_rock = Sprite(random_pos, random_velocity, 0, random_ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
     
# helper method to udpate a sprite group
def process_sprite_group(sprite_group, canvas):
    for a_sprite in set(sprite_group):        
        a_sprite.draw(canvas)
        remove_it = a_sprite.update()
        if remove_it:
            sprite_group.remove(a_sprite)
     
# helper method for group collisions
def group_collide(group, other_object):
    global explosion_group
    collisions = 0
    for obj in set(group):
        if obj.collide(other_object):
            group.remove(obj)
            collisions += 1
            explosion = Sprite(obj.pos, [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)    
    return collisions
        
# helper method for group-group collision
def group_group_collide(group_a, group_b):
    collisions = 0
    for obj in set(group_a):
        if group_collide(group_b, obj) > 0:
            group_a.remove(obj)
            collisions += 1            
    return collisions

# initialize ship and two sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouse_handler)
frame.set_draw_handler(draw)

# create timer
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
