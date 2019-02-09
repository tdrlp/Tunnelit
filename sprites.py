# Tunnelit: The Best Game Ever
# By Tudor Lupu
# FILE CONTAINTING ALL THE SPRITE CLASSES
import pygame as pg
import time, glob
from settings import *

class Player(pg.sprite.Sprite):
    # Player Sprite Class
    def __init__(self, x, y, player):
        pg.sprite.Sprite.__init__(self)
        # load all the images for the animations
        self.load_images()
        # set the initial frames for all the players
        if player == "player1":
            self.image = pg.image.load(self.walk_frames_bp1[0])
        else:
            self.image = pg.image.load(self.walk_frames_bp2[0])
        # create the rect for the players
        self.rect = self.image.get_rect()
        # bool to check if the player is walking
        self.walking = False
        # current frame of the animation
        self.current_frame = 0
        # last time the animation was updated
        self.last_update = 0

        # place the player on the screen
        self.rect.x = x
        self.rect.y = y
        # set the player speed
        self.change_in_x = PLAYERSPEED
        self.change_in_y = PLAYERSPEED
        # the direction the player is heading
        self.direction = "None"
        # contains if player 1 or 2
        self.player = player
        # set the player lives
        self.lives = 2

    def load_images(self):
        # load the animations for player 1 walking backwards
        self.walk_frames_bp1 = glob.glob("Animations\Player1\Backwarads\move*.png")
        self.walk_frames_bp1.sort()
        # load the animations for player 2 walking backwards
        self.walk_frames_bp2 = glob.glob("Animations\Player2\Backwarads\move*.png")
        self.walk_frames_bp2.sort()
        # load the animations for player 1 walking forward
        self.walk_frames_up1 = glob.glob("Animations\Player1\Forward\move*.png")
        self.walk_frames_up1.sort()
        # load the animations for player 2 walking forward
        self.walk_frames_up2 = glob.glob("Animations\Player2\Forward\move*.png")
        self.walk_frames_up2.sort()
        # load the animations for player 1 walking right
        self.walk_frames_rp1 = glob.glob("Animations\Player1\Right-Left\move*.png")
        self.walk_frames_rp1.sort()
        # load the animations for player 2 walking right
        self.walk_frames_rp2 = glob.glob("Animations\Player2\Right-Left\move*.png")
        self.walk_frames_rp2.sort()

        # go through the walking right animations and flip them to create left animations for player 1
        self.walk_frames_lp1 = []
        for frame in self.walk_frames_rp1:
            self.walk_frames_lp1.append(pg.transform.flip(pg.image.load(frame), True, False))
        # go through the walking right animations and flip them to create left animations for player 1
        self.walk_frames_lp2 = []
        for frame in self.walk_frames_rp2:
            self.walk_frames_lp2.append(pg.transform.flip(pg.image.load(frame), True, False))

    def update(self):
        # animate the player when walking
        self.animate()
        # get the key pressed
        keystate = pg.key.get_pressed()
        # check player 1 controls for WASD and set the direction the player is walking
        if self.player == "player1":
            if keystate[pg.K_a]:
                self.rect.x -= self.change_in_x
                self.direction = "Left"
                self.walking = True
            elif keystate[pg.K_d]:
                self.rect.x += self.change_in_x
                self.direction = "Right"
                self.walking = True
            elif keystate[pg.K_w]:
                self.rect.y -= self.change_in_y
                self.direction = "Up"
                self.walking = True
            elif keystate[pg.K_s]:
                self.rect.y += self.change_in_y
                self.direction = "Down"
                self.walking = True
            else:
                self.direction = "None"
                self.walking = False
        # check player 2 controls for ARROWS and set the direction the player is walking
        elif self.player == "player2":
            if keystate[pg.K_LEFT]:
                self.rect.x -= self.change_in_x
                self.direction = "Left"
                self.walking = True
            elif keystate[pg.K_RIGHT]:
                self.rect.x += self.change_in_x
                self.direction = "Right"
                self.walking = True
            elif keystate[pg.K_UP]:
                self.rect.y -= self.change_in_y
                self.direction = "Up"
                self.walking = True
            elif keystate[pg.K_DOWN]:
                self.rect.y += self.change_in_y
                self.direction = "Down"
                self.walking = True
            else:
                self.direction = "None"
                self.walking = False

    def animate(self):
        # get the current game ticks
        now = pg.time.get_ticks()
        if self.walking:    # if the player is walking
            # update the animation if 100 ticks have passed
            if now - self.last_update > 100:
                # update the animations for player 1
                if self.player == "player1":
                    if self.direction == "Down":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_bp1)
                        self.image = pg.image.load(self.walk_frames_bp1[self.current_frame])
                    if self.direction == "Up":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_up1)
                        self.image = pg.image.load(self.walk_frames_up1[self.current_frame])
                    if self.direction == "Right":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_rp1)
                        self.image = pg.image.load(self.walk_frames_rp1[self.current_frame])
                    if self.direction == "Left":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_lp1)
                        self.image = self.walk_frames_lp1[self.current_frame]

                # update the animations for player 2
                if self.player == "player2":
                    if self.direction == "Down":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_bp2)
                        self.image = pg.image.load(self.walk_frames_bp2[self.current_frame])
                    if self.direction == "Up":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_up2)
                        self.image = pg.image.load(self.walk_frames_up2[self.current_frame])
                    if self.direction == "Right":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_rp2)
                        self.image = pg.image.load(self.walk_frames_rp2[self.current_frame])
                    if self.direction == "Left":
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_lp2)
                        self.image = self.walk_frames_lp2[self.current_frame]

        else:
            # if the player is not moving reset him to be facing up
            if self.player == "player1":
                self.image = pg.image.load(self.walk_frames_bp1[0])
            else:
                self.image = pg.image.load(self.walk_frames_bp2[0])

class Bomb(pg.sprite.Sprite):
    # Bomb Sprite Class
    def __init__(self, x, y, colour):
        pg.sprite.Sprite.__init__(self)
        # set the bomb image
        self.image, self.rect = load_image("bomb.png")
        # place the bomb at the middle of the player
        self.rect.centerx = x
        self.rect.centery = y
        # start the counter
        self.start_time = time.time()
        # check if the bomb exploded
        self.exploded = False
        # check if the sound for explosion played already
        self.playedsound = False
        # create the sound for the explosion
        self.bomb_sound = pg.mixer.Sound("Sound/bombexplosion.wav")

    def update(self):
        # get current time
        self.end_time = time.time()
        # check if 3  seconds passed
        if self.end_time - self.start_time > 3:
            if not self.playedsound:
                # play the explosion sound if didnt already
                self.bomb_sound.play()
                self.playedsound = True
            # turn the bomb into the explosion
            self.image = pg.image.load("explosions/middle.png").convert_alpha()
            if self.end_time - self.start_time > 5:
                # reset everything and destroy the bomb
                self.start_time = time.time()
                self.playedsound = False
                self.exploded = True
                self.kill()

class TopBotBomb(pg.sprite.Sprite):
    # Top and Bottom of the Bomb Sprite Class
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # create the image for the explosion
        self.image, self.rect = load_image("explosions/explosion_topbot.png")
        # place it according to the bomb
        self.rect.x = x
        self.rect.y = y
        self.start_time = time.time()

    def update(self):
        self.end_time = time.time()
        # check if 2 seconds passed and destroy the explosion
        if self.end_time - self.start_time > 2:
            self.start_time = time.time()
            self.kill()


class LeftRigthBomb(pg.sprite.Sprite):
    # Left and Right sides of the Bomb Sprite Class
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # create the image for the explosion
        self.image, self.rect = load_image("explosions/explosion_side.png")
        # place it according to the bomb
        self.rect.x = x
        self.rect.y = y
        self.start_time = time.time()

    def update(self):
        self.end_time = time.time()
        # check if 2 seconds passed and destroy the explosion
        if self.end_time - self.start_time > 2:
            self.start_time = time.time()
            self.kill()


class Wallblocks(pg.sprite.Sprite):
    # Blocks Sprite Class
    def __init__(self, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        # load the image according to what block it is
        self.image, self.rect = load_image(filename)
        # place it
        self.rect.x = x
        self.rect.y = y

def load_image(filename):
    # load the images and get the rect for it
        image = pg.image.load(filename).convert_alpha()
        return image, image.get_rect()
