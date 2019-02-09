# Tunnelit: The Best Game Ever
# This game is a much worse version of the original bomberman.
# By Tudor Lupu - 2016
import pygame as pg # create a shortcut so instead of pygame i just write pg
import random, time, os
from settings import *
from sprites import *
from pygame.locals import *

class Game:
    def __init__(self):
        # initialize game window, etc
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        # initialize pygame
        pg.init()
        # initialize the mixer for music
        pg.mixer.init()
        # set the screen size
        self.screen = pg.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
        # set the name of the game
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # set the game to running
        self.running = True
        # set the font used
        self.font_name = pg.font.match_font(FONT_NAME)
        # create the sound effects used
        self.bomb_place = pg.mixer.Sound("Sound/bombplace.wav")
        self.hitbybomb = pg.mixer.Sound("Sound/lostlife.wav")

    def new(self):
        # start a new game
        # CREATE ALL THE SPRITE GROUPS
        self.ctblocks = pg.sprite.Group()   # group for all the blocks that cant be walked over
        self.blocks = pg.sprite.Group() # group for all the blocks that can be walked over
        self.destroy = pg.sprite.Group()    # group for all the destroyable blocks
        self.all_sprites = pg.sprite.Group()    # group for all the sprites
        self.bombs = pg.sprite.Group()  # group for all the bombs
        self.player1bombs = pg.sprite.Group()   # group for player1's bombs
        self.player2bombs = pg.sprite.Group()   # group for player2's bombs
        self.explosions = pg.sprite.Group() # group for the bomb explosion sides

        # start the game timer
        self.game_time = time.time()
        self.update_time = 0

        # set game time values
        self.seconds = 60
        self.minutes = 3

        # create the players
        self.player1 = Player(90, 145, "player1")
        self.player2 = Player(690, 545, "player2")
        # add the players to the all sprites group
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        # create the map from the list given
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                # add all the grass blocks to the blocks group
                if tilemap[row][column] != MIDBLOCK and tilemap[row][column] != SIDEBLOCK and tilemap[row][column] != DBLOCK:
                    self.block = Wallblocks((column*TILESIZE)+35, (row*TILESIZE)+90, "blocks/grass.png")
                    self.blocks.add(self.block)
                # add all the side blocks to the cant touch block group.
                if tilemap[row][column] == SIDEBLOCK:
                    self.block = Wallblocks((column*TILESIZE)+35, (row*TILESIZE)+90,  "blocks/sideblock.png")
                    self.ctblocks.add(self.block)
                # add the midblocks to the cant touch block group. adding them separately looks nicer when drawing them:)
                if tilemap[row][column] == MIDBLOCK:
                    self.block = Wallblocks((column*TILESIZE)+35, (row*TILESIZE)+90,  "blocks/midblock.png")
                    self.ctblocks.add(self.block)
                # add the blocks that can be destroyed to the destroy group
                if tilemap[row][column] == DBLOCK:
                    self.block = Wallblocks((column*TILESIZE)+35, (row*TILESIZE)+90, "blocks/brick.png")
                    self.destroy.add(self.block)
        # load the game music
        pg.mixer.music.load("Sound/intense_music.ogg")
        # run the game
        self.run()

    def run(self):
        # Game Loop
        # start playing the game music. infinite loop
        pg.mixer.music.play()
        self.playing = True
        # run the game while the user is playing
        while self.playing:
            self.clock.tick(FRAMERATE)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        current_time = time.time()
        counter = 0
        self.all_sprites.update()
        #check player collision with the the side and mid blocks
        self.check_player_collision(self.player1, self.ctblocks)
        self.check_player_collision(self.player2, self.ctblocks)

        # check player collision with the destroyable blocks
        self.check_player_collision(self.player1, self.destroy)
        self.check_player_collision(self.player2, self.destroy)

        # check player collision with the enemy bombs
        self.check_player_collision(self.player1, self.player2bombs)
        self.check_player_collision(self.player2, self.player1bombs)

        # check player1 collision with the bombs
        self.check_player_explosion(self.player1)
        if self.player1.lives <1:
            self.player1.kill()
            self.playing = False
            self.show_go_screen()
        # check player2 collision with the bombs
        self.check_player_explosion(self.player2)
        if self.player2.lives <1:
            self.player2.kill()
            self.playing = False
            self.show_go_screen()

        # check if the explosion touches the destoyable blocks
        self.check_block_explosion(self.destroy, self.explosions)

        current_time = time.time()
        # check if the time ran out
        if self.seconds == 59 and self.minutes < 0:
            self.playing = False
            self.show_go_screen()
        # check if a second passed
        if current_time - self.update_time > 1:
            self.seconds -= 1
            self.update_time = current_time
        # update minutes after 60 seconds passed
        if self.seconds == 0:
            self.minutes -= 1
            self.seconds = 59

    def check_player_collision(self, player, blocks):
        # check player collision with blocks its not supposed to walk over
        for b in blocks:
            if player.rect.colliderect(b.rect):
                # check the right side of the player
                if player.direction == "Right":
                    player.rect.x -= player.change_in_x
                # check the left side of the player
                if player.direction == "Left":
                    player.rect.x += player.change_in_x
                # check the upper side of the player
                if player.direction == "Up":
                    player.rect.y += player.change_in_y
                # check the bottom side of the player
                if player.direction == "Down":
                    player.rect.y -= player.change_in_y

    def check_player_explosion(self, player):
        # check if the explosion collided with the player
        for b in self.explosions:
            if player.rect.colliderect(b.rect):
                # play hit by bomb sound
                self.hitbybomb.play()
                # player loses one life
                player.lives -= 1
                # that side of the explosion dissapears
                b.kill()

    def check_block_explosion(self, blocks, explosions):
        # check for explosion collision with destroyable blocks
        for b in blocks:
            for exp in explosions:
                # check collision
                if b.rect.colliderect(exp.rect):
                    # destroy the block
                    b.kill()

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            # check if the player wants to quit the game
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # check for a key press
            if event.type == pg.KEYDOWN:
                # check if space was pressed
                if event.key == pg.K_SPACE:
                    # play bomb place sound
                    self.bomb_place.play()

                    # create new bomb
                    b = Bomb(self.player1.rect.centerx, self.player1.rect.centery, BLACK)
                    self.all_sprites.add(b)
                    self.bombs.add(b)
                    self.player1bombs.add(b)

                # check if 0 was pressed
                if event.key == pg.K_KP0:
                    # play bomb place sound
                    self.bomb_place.play()

                    # create new bomb
                    b = Bomb(self.player2.rect.centerx, self.player2.rect.centery, PURPLE)
                    self.all_sprites.add(b)
                    self.bombs.add(b)
                    self.player2bombs.add(b)

        self.current_time = time.time()
        # create the sides of the bomb for explosion
        for b in self.bombs:
            if not b.exploded:
                # check if 3 seconds have passed
                if self.current_time - b.start_time > 3:
                    # create the right side explosion
                    bright = LeftRigthBomb(b.rect.x+24, b.rect.y)
                    self.explosions.add(bright)
                    self.all_sprites.add(bright)

                    # create the upper side explosion
                    btop = TopBotBomb(b.rect.x, b.rect.y-48)
                    self.explosions.add(btop)
                    self.all_sprites.add(btop)

                    # create the left side explosion
                    bleft = LeftRigthBomb(b.rect.x-48, b.rect.y)
                    self.explosions.add(bleft)
                    self.all_sprites.add(bleft)

                    # create the bottom side explosion
                    bbot = TopBotBomb(b.rect.x, b.rect.y+24)
                    self.explosions.add(bbot)
                    self.all_sprites.add(bbot)
                    b.exploded = True

    def draw(self):
        # Game Loop - Draw
        # draw the game background
        self.screen.blit(BACKGROUND, (0, 0))
        # draw the player lives
        self.draw_text(str(self.player1.lives), 27, WHITE, 295, 27)
        self.draw_text(str(self.player2.lives), 27, WHITE, WINDOWWIDTH-243, 27)
        # draw the fps
        self.draw_text("FPS:", 24, WHITE, 40, 10)
        self.draw_text(str(int(self.clock.get_fps())), 24, WHITE, 80, 10)
        # draw the timer
        self.draw_text(str(self.minutes), 24, WHITE, WINDOWWIDTH/2-15, 27)
        self.draw_text(":", 24, WHITE, WINDOWWIDTH/2, 27)
        # check if the seconds are less than 0 to add another 0 for a nicer format
        if self.seconds < 10:
            self.draw_text("0"+str(self.seconds), 24, WHITE, WINDOWWIDTH/2+20, 27)
        else:
            self.draw_text(str(self.seconds), 24, WHITE, WINDOWWIDTH/2+20, 27)
        # draw all the sprites and blocks separately
        self.blocks.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.ctblocks.draw(self.screen)
        self.destroy.draw(self.screen)

        # flip the display after drawing everything
        pg.display.flip()

    def show_start_screen(self):
        # Show the Start Screen
        # play the intro music
        pg.mixer.music.load("Sound/Dream.mp3")
        # play the music with an infinite loop
        pg.mixer.music.play()
        # display the instructions and everything
        self.screen.blit(INTRO, (0, 0))
        # flip the display after drawing everything
        pg.display.flip()
        # wait for user to press any key
        self.wait_for_key()
        # stop the intro music
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # Show the Game Over screen
        # stop the game music
        pg.mixer.music.stop()
        # check if the game is still running
        if not self.running:
            return
        # load and play the game over music
        pg.mixer.music.load("Sound/Dream.mp3")
        pg.mixer.music.play()
        # display the player 2 win screen
        if self.player1.lives <1:
            self.screen.blit(P2WIN, (0, 0))
        # display the player 1 win screen
        elif self.player2.lives <1:
            self.screen.blit(P1WIN, (0, 0))
        # display the time ran out screen
        else:
            self.screen.blit(BOTHLOSE, (0, 0))
        # flip the display after drawing everything
        pg.display.flip()
        # wait for the user to press any key
        self.wait_for_key()
        # stop the game over music
        pg.mixer.music.stop()

    def wait_for_key(self):
        # set bool for waiting for user to press a key
        waiting = True
        while waiting:
            self.clock.tick(FRAMERATE)
            for event in pg.event.get():
                # check if the user wants to quit
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                # check if the user pressed a key
                if event.type == pg.KEYDOWN:
                    # stop waiting
                    waiting = False
                    # start new game
                    self.new()

    def draw_text(self, text, size, color, x, y):
        # create the text font
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        # create the rect for the text
        text_rect = text_surface.get_rect()
        # place the text where the user wants
        text_rect.midtop = (x, y)
        # draw the text on the screen
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
BACKGROUND = BACKGROUND.convert_alpha()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
