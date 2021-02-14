import pygame as pg
from sys import exit
from random import randint, choice
from math import sqrt, pow, atan
from time import sleep, time, localtime, asctime

pg.init()
scr_wid = 1200
scr_hgt = 700
screen = pg.display.set_mode((scr_wid, scr_hgt))
pg.display.set_caption("Karlo's struggle 1")
title_icon = pg.image.load("yellow.png")
pg.display.set_icon(title_icon)


vol_bgm = 0.05
vol_click = 0.15
vol_Kill_bot = 0.35
vol_gameover = 0.35
pg.mixer.music.load('_bgm.ogg')
click_sound = pg.mixer.Sound('click.ogg')
kill_bot_sound = pg.mixer.Sound('kill_bot.ogg')
gameover_sound = pg.mixer.Sound('gameover.ogg')
pg.mixer.music.set_volume(vol_bgm)
click_sound.set_volume(vol_click)
kill_bot_sound.set_volume(vol_Kill_bot)
gameover_sound.set_volume(vol_gameover)

pg.mixer.music.play(-1)
music_on = True
sound_on = True

black = [0, 0, 0]
white = [255, 255, 255]
clock = pg.time.Clock()
chaser_wid = chaser_hgt = 35
player_wid = player_hgt = 40
tower_wid = tower_hgt = 70
Chaser_Player_r = 25
Tower_Player_r = 50
laser_range = 300
laser_width = 12
laser_kill_range = 20
die_wid = 70
die_hgt = 70
die = pg.image.load("star.png")
die = pg.transform.smoothscale(die, (die_wid, die_hgt))
score = 0
fps = 60
chaser_speed = 4
Gameover = False
H_page = False
A_page = False
St_page = False
SB_page = False
MnLp = False
min_dst = 40
bot_num = 8
gamemode = 'normal'
pos_yes_icon = [80, 300]
num_lst = []

def load_SB(file):
    with open(file, 'r') as f:
        f_lst = f.readlines()
        SB = [
            [int(f_lst[0][:-1]), f_lst[1][:-1]], [int(f_lst[2][:-1]), f_lst[3][:-1]], 
            [int(f_lst[4][:-1]), f_lst[5][:-1]], [int(f_lst[6][:-1]), f_lst[7][:-1]], 
            [int(f_lst[8][:-1]), f_lst[9][:-1]], [int(f_lst[10][:-1]), f_lst[11][:-1]], 
            [int(f_lst[12][:-1]), f_lst[13][:-1]], [int(f_lst[14][:-1]), f_lst[15][:-1]]
                ]
        return SB

E_SB = load_SB(file='_e_sb.txt')
N_SB = load_SB(file='_n_sb.txt')
H_SB = load_SB(file='_h_sb.txt')
I_SB = load_SB(file='_i_sb.txt')

def save_all_SB():
    def save_SB(file, SB):
        SB = [
            str(SB[0][0]), SB[0][1], str(SB[1][0]), SB[1][1],
            str(SB[2][0]), SB[2][1], str(SB[3][0]), SB[3][1],
            str(SB[4][0]), SB[4][1], str(SB[5][0]), SB[5][1],
            str(SB[6][0]), SB[6][1], str(SB[7][0]), SB[7][1]
            ]
        with open(file, 'w') as f:
            for i in SB:
                f.writelines(i)
                f.write('\n')
    save_SB('_e_sb.txt', E_SB)
    save_SB('_n_sb.txt', N_SB)
    save_SB('_h_sb.txt', H_SB)
    save_SB('_i_sb.txt', I_SB)

def clear_all_SB():
    global E_SB, N_SB, H_SB, I_SB
    E_SB= [[0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0']]
    N_SB= [[0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0']]
    H_SB= [[0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0']]
    I_SB= [[0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0'], [0, '0']]
    def clear_SB(file):
        with open(file, 'w') as f:
            for i in range(16):
                f.writelines('0')
                f.write('\n')
    clear_SB('_e_sb.txt')
    clear_SB('_n_sb.txt')
    clear_SB('_h_sb.txt')
    clear_SB('_i_sb.txt')

class Me(object):
    def __init__(self, pos=[500, 400]):
        self.pos = pos
        self.ctpos = [self.pos[0]+player_wid/2, self.pos[1]+tower_hgt/2] 
        self.player = pg.image.load("playerblue.png")
        self.player = pg.transform.smoothscale(self.player, (player_wid, player_hgt))
        self.W = False
        self.A = False
        self.S = False
        self.D = False
        self.a = 0.4
        self.Uv = 0
        self.Rv = 0
    def event_response(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_all_SB()
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.W = True
                if event.key == pg.K_LEFT:
                    self.A = True
                if event.key == pg.K_DOWN:
                    self.S = True
                if event.key == pg.K_RIGHT:
                    self.D = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.W = False
                if event.key == pg.K_LEFT:
                    self.A = False
                if event.key == pg.K_DOWN:
                    self.S = False
                if event.key == pg.K_RIGHT:
                    self.D = False
        if self.W == True:
            self.Uv = self.Uv + self.a
        if self.A == True:
            self.Rv = self.Rv - self.a
        if self.S == True:
            self.Uv = self.Uv - self.a
        if self.D == True:
            self.Rv = self.Rv + self.a
        self.pos = [self.pos[0]+self.Rv, self.pos[1]-self.Uv]   
        self.ctpos = [self.pos[0]+player_wid/2, self.pos[1]+tower_hgt/2]
    def detect_out(self):
        if self.pos[0] < -40 or self.pos[0] > scr_wid-player_wid+40 or self.pos[1] < -40 or\
        self.pos[1] > scr_hgt-player_hgt+40:
            global Gameover
            Gameover = True
    def rotate(self):
        self.new_me = self.player
        #pg.draw.line(screen, [0, 255, 0], self.ctpos, [self.ctpos[0], self.ctpos[1]-self.Uv*20], laser_width)
        #pg.draw.line(screen, [255, 0, 0], self.ctpos, [self.ctpos[0]+self.Rv*20, (self.ctpos[1])], laser_width)
        if not self.Uv == 0:
            tanA = self.Rv/self.Uv
            angle = atan(tanA)*180/3.14
            if self.Uv > 0:
                self.new_me = pg.transform.rotate(self.player, -angle)
            else:
                self.new_me = pg.transform.rotate(self.player, -angle+180)
        else:
            if self.Rv > 0:
                self.new_me = pg.transform.rotate(self.player, -90)
            else:
                self.new_me = pg.transform.rotate(self.player, 90)

    def draw(self):
        screen.blit(self.new_me, self.pos)
    def me_go(self):
        me.event_response()
        me.detect_out()
        me.rotate()
        me.draw()

me = Me()   

class Tower(object):
    def __init__(self, pos = [0, 0]):
        self.pos = pos   
        self.tower = pg.image.load("_tower.png")
        self.tower = pg.transform.smoothscale(self.tower, (tower_wid, tower_hgt))
        self.ctpos = [self.pos[0]+tower_wid/2, self.pos[1]+tower_hgt/2] 
    def detect_player(self):
        if sqrt(pow(me.pos[0]-self.pos[0], 2)+pow(me.pos[1]-self.pos[1], 2)) < Tower_Player_r:
            global Gameover
            Gameover = True
    def laser(self):
        if sqrt(pow(me.pos[0]-self.pos[0], 2)+pow(me.pos[1]-self.pos[1], 2)) < laser_range:
            pg.draw.line(screen, [randint(0, 200), randint(0, 200), randint(0, 200)],
                        self.ctpos, me.ctpos, laser_width)
    def draw(self):
        screen.blit(self.tower, self.pos) 

tower1 = Tower([scr_wid/4 - tower_wid/2 + 20, scr_hgt/4 - tower_hgt/2 + 20])
tower2 = Tower([3*scr_wid/4 - tower_wid/2 + 20, scr_hgt/4 - tower_hgt/2 - 20])
tower3 = Tower([3*scr_wid/4 - tower_wid/2 - 20, 3*scr_hgt/4 - tower_hgt/2 - 20]) 
tower4 = Tower([scr_wid/4 - tower_wid/2 - 20, 3*scr_hgt/4 - tower_hgt/2 + 20])
Towers = [tower1, tower2, tower3, tower4]

class Chaser(object):
    def __init__(self, pos=[0, 0]):
        self.pos = pos
        self.ctpos = [self.pos[0]+chaser_wid/2, self.pos[1]+chaser_hgt/2] 
        self.edge_point = [self.pos, [self.pos[0]+chaser_wid, self.pos[1]], \
                        [self.pos[0]+chaser_wid, self.pos[1]+chaser_hgt], [self.pos[0], self.pos[1]+chaser_hgt]]
        self.chaser = pg.image.load("_red.png")
        self.chaser = pg.transform.smoothscale(self.chaser, (chaser_wid, chaser_hgt))
    def chase(self):
        x = self.pos[0]-me.pos[0]
        y = self.pos[1]-me.pos[1]
        l = sqrt(pow(x, 2) + pow(y, 2))
        ratio = chaser_speed/l
        x_mov = x*ratio
        y_mov = y*ratio
        self.pos[0] = self.pos[0] - x_mov
        self.pos[1] = self.pos[1] - y_mov
        self.ctpos = [self.pos[0]+chaser_wid/2, self.pos[1]+chaser_hgt/2]
        self.edge_point = [self.pos, [self.pos[0]+chaser_wid, self.pos[1]], \
                        [self.pos[0]+chaser_wid, self.pos[1]+chaser_hgt], [self.pos[0], self.pos[1]+chaser_hgt]]
    def detect_player(self):        
        if sqrt(pow(me.pos[0]-self.pos[0], 2)+pow(me.pos[1]-self.pos[1], 2)) < Chaser_Player_r:
            global Gameover
            Gameover = True
    def rotate(self):
        if not (me.pos[1]-self.pos[1]) == 0:
            tanA = (me.pos[0]-self.pos[0])/(me.pos[1]-self.pos[1])
            angle = atan(tanA)*180/3.14
            if self.pos[1] > me.pos[1]:
                self.new_chaser = pg.transform.rotate(self.chaser, angle)
            else:
                self.new_chaser = pg.transform.rotate(self.chaser, angle+180)
        else:
            if self.pos[0] > me.pos[0]:
                self.new_chaser = pg.transform.rotate(self.chaser, 90)
            else:
                self.new_chaser = pg.transform.rotate(self.chaser, -90)
    def draw(self):
        screen.blit(self.new_chaser, self.pos) 

class Txt_info(object):
    def __init__(self, style = 'consolas', color = [230, 230, 230]):
        self.style = style
        self.color = color
        self.bg_color = black
    def draw_score_board(self, pos, size):
        self.ft = pg.font.SysFont(self.style, size)
        self.pos = pos
        text = self.ft.render('score:{s}'.format(s=score), True, self.color, self.bg_color)
        screen.blit(text, self.pos) 
    def draw_info(self, info, pos, size):
        self.ft = pg.font.SysFont(self.style, size)
        self.size = size
        self.pos = pos
        text = self.ft.render(info, True, self.color, self.bg_color)
        screen.blit(text, self.pos) 

score_board = Txt_info()
common_txt = Txt_info()

def tower_go():
    for each_tower in Towers:
        each_tower.detect_player()
        each_tower.laser()
        each_tower.draw()   

def Bubble_Sort(lst):
    for freq in range(1, len(lst)):
        for each_elmt in range(0, len(lst)-1):
            if lst[each_elmt] < lst[each_elmt+1]:
                lst[each_elmt], lst[each_elmt+1]=lst[each_elmt+1], lst[each_elmt]
    return lst            

def refresh_SB():
    global E_SB, N_SB, H_SB, I_SB
    def refresh_one_SB(SB, mod):
        global num_lst
        if gamemode == mod:
            num_lst = [SB[0][0], SB[1][0], SB[2][0], SB[3][0], SB[4][0], SB[5][0], SB[6][0], SB[7][0]]
            if score > min(num_lst):
                SB[7] = [score, asctime(localtime(time()))]
                Bubble_Sort(SB)
    refresh_one_SB(E_SB, 'easy')
    refresh_one_SB(N_SB, 'normal')
    refresh_one_SB(H_SB, 'hard')
    refresh_one_SB(I_SB, 'hell')

def main_loop():
    global score, MnLp
    score = 0
    timer = 0
    Chasers = []
    Chasers_ctpos = []
    me.pos = [500, 400]
    me.Rv = me.Uv = 0
    for i in range(bot_num):
        chaser = Chaser(choice([[randint(0, scr_wid), scr_hgt], [randint(0, scr_wid), -50], \
                                [-30, randint(0, scr_hgt)], [scr_wid, randint(0, scr_hgt)]]))
        Chasers.append(chaser)
        Chasers_ctpos.append(chaser.ctpos)   
    me.W = me.A = me.S = me.D = False    
    def end_page():
        global Gameover, MnLp
        me.Rv = 0
        me.Uv = 0
        common_txt.draw_info('Game Over!', pos = [500, 160], size = 30)
        common_txt.draw_info('Your score is {s} :) mode:{m}'
                            .format(s=score, m=gamemode), pos = [330, 260], size = 30)
        common_txt.draw_info('Restart (R)', pos = [500, 360], size = 30)
        common_txt.draw_info('Main menu (M)', pos = [490, 460], size = 30)
        common_txt.draw_info('Quit (Q)', pos = [520, 560], size = 30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_all_SB()
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    click_sound.play()
                    save_all_SB()
                    pg.quit()
                    exit()  
                if event.key == pg.K_r:  
                    click_sound.play()
                    Gameover = False
                if event.key == pg.K_m:  
                    click_sound.play()
                    Gameover = False
                    MnLp = False        
        pg.display.update()
        screen.fill(black)
        clock.tick(fps)

    while True:
        score_board.draw_score_board([0, 0], size = 26)
        common_txt.draw_info('{mod}'.format(mod = gamemode), pos = [150, 0], size = 26)
        timer = timer + 1
        if timer > 15:
            timer = 0
            score = score + 1
        tower_go()

        #####
        t = 0
        for each_bot in Chasers:
            for EACH_TOWER in Towers:

                if sqrt(pow(EACH_TOWER.pos[0]-each_bot.pos[0], 2) +\
                        pow(EACH_TOWER.pos[1]-each_bot.pos[1], 2)) < Tower_Player_r:
                    ex = EACH_TOWER.pos[0] - each_bot.pos[0]
                    ey = EACH_TOWER.pos[1] - each_bot.pos[1]
                    e_ratio = 8 / Tower_Player_r
                    x_back = ex*e_ratio
                    y_back = ey*e_ratio
                    each_bot.pos[0] = each_bot.pos[0] - x_back
                    each_bot.pos[1] = each_bot.pos[1] - y_back

                x1 = me.pos[0]
                y1 = me.pos[1]
                x2 = EACH_TOWER.pos[0]
                y2 = EACH_TOWER.pos[1]
                x3 = each_bot.pos[0]
                y3 = each_bot.pos[1]
                if not x1-x2 == 0:
                    k = (y1-y2)/(x1-x2)
                b = y1 - k*x1
                d = sqrt(pow(-k*x3+y3-b, 2))/sqrt(pow(k, 2)+1)
                D_pt = sqrt(pow(me.pos[0]-EACH_TOWER.pos[0], 2)+pow(me.pos[1]-EACH_TOWER.pos[1], 2))
                D_bt = sqrt(pow(each_bot.pos[0]-EACH_TOWER.pos[0], 2)+pow(each_bot.pos[1]-EACH_TOWER.pos[1], 2))
                D_pb = sqrt(pow(me.pos[0]-each_bot.pos[0], 2)+pow(me.pos[1]-each_bot.pos[1], 2))
                if d < laser_kill_range and D_pt > D_bt and D_pt < laser_range and D_pb < D_pt:
                    score = score + 10
                    die_pos = [each_bot.pos[0]-13, each_bot.pos[1]-12]
                    kill_bot_sound.play()
                    each_bot.pos = choice([[randint(0, scr_wid), scr_hgt], [randint(0, scr_wid), -50], \
                                        [-30, randint(0, scr_hgt)], [scr_wid, randint(0, scr_hgt)]])
                    screen.blit(die, die_pos)

            Chasers_ctpos.pop(t)
            for other_ctpos in Chasers_ctpos:
                if other_ctpos[0]-each_bot.ctpos[0] == other_ctpos[1]-each_bot.ctpos[1] == 0:
                    each_bot.ctpos[0] = each_bot.ctpos[0] - 1
                    each_bot.ctpos[1] = each_bot.ctpos[1] - 1
                ex = other_ctpos[0]-each_bot.ctpos[0]
                ey = other_ctpos[1]-each_bot.ctpos[1]   
                dst = sqrt(pow(ex, 2)+pow(ey, 2))
                if dst < min_dst:
                    e_ratio = 2/dst
                    x_back = ex*e_ratio
                    y_back = ey*e_ratio
                    each_bot.pos[0] = each_bot.pos[0] - x_back
                    each_bot.pos[1] = each_bot.pos[1] - y_back
            Chasers_ctpos.insert(t, each_bot.ctpos)  
            t = t + 1      
            each_bot.chase()            
            each_bot.rotate()
            each_bot.draw()
            each_bot.detect_player() 
        #####

        me.me_go()
        pg.display.update()
        screen.fill(black)
        clock.tick(fps)
        if Gameover == True:
            gameover_sound.play()
            refresh_SB()
            for i in range(10):
                sleep(0.1)
                tower_go()
                pg.display.update()
                screen.fill([randint(0, 100), 0, 0]) 
            break

    while Gameover == True:
        end_page()

def Start_page():
    global MnLp, St_page, SB_page, A_page, H_page
    title = pg.image.load("_title.png")
    title = pg.transform.smoothscale(title, (scr_wid, 370))
    screen.blit(title, [0, 0])
    common_txt.draw_info('difficulty:{mod}'.format(mod = gamemode), pos = [10, scr_hgt-30], size = 26)
    common_txt.draw_info('Play (P)', pos = [520, 370], size = 30)
    common_txt.draw_info('settings (T)', pos = [480, 420], size = 30)
    common_txt.draw_info('score board (S)', pos = [460, 470], size = 30)
    common_txt.draw_info('Author (A)', pos = [500, 520], size = 30)
    common_txt.draw_info('Help (H)', pos = [520, 570], size = 30)
    common_txt.draw_info('Quit (Q)', pos = [520, 620], size = 30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            save_all_SB()
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            click_sound.play()
            if event.key == pg.K_p:
                MnLp = True
            if event.key == pg.K_t:  
                St_page = True
            if event.key == pg.K_s:
                SB_page = True
            if event.key == pg.K_a:
                A_page = True
            if event.key == pg.K_h:
                H_page = True
            if event.key == pg.K_q:
                save_all_SB()
                pg.quit()
                exit()
    pg.display.update()
    screen.fill(black)
    clock.tick(fps)
    
def Help_page():
    global H_page
    common_txt.draw_info('*Use W, A, S, D to control Karlo', pos = [100, 200], size = 30)
    common_txt.draw_info('*Avoid borders, enemies and laser towers', pos = [100, 250], size = 30)
    common_txt.draw_info('*Get close to laser towers to activate destructive laser', pos = [100, 300], size = 30)
    common_txt.draw_info('*Use laser to kill enemies and get points', pos = [100, 350], size = 30)
    common_txt.draw_info('*Points will increase automatically as long as you are alive', pos = [100, 400], size = 30)
    common_txt.draw_info('*ONE LIFE only, good luck :)', pos = [100, 450], size = 30)
    common_txt.draw_info('Main menu (M)', pos = [100, 550], size = 30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            save_all_SB()
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            click_sound.play()
            if event.key == pg.K_m:
                H_page = False
    pg.display.update()
    screen.fill(black)
    clock.tick(fps)

def Author_page():
    global A_page
    common_txt.draw_info('Program: Jiamin', pos = [300, 200], size = 30)
    common_txt.draw_info('Art&Sound: Jiamin', pos = [300, 250], size = 30)
    common_txt.draw_info('Music: Motion Focus Music', pos = [300, 300], size = 30)
    common_txt.draw_info('Test: Jiamin', pos = [300, 350], size = 30)
    common_txt.draw_info('Thanks for paying attention to this game, if having any idea or suggestion, ', \
                        pos = [200, 400], size = 20)
    common_txt.draw_info('contact us through the email:', pos = [200, 430], size = 20)
    common_txt.draw_info('jiaming2001_new@outlook.com', pos = [300, 480], size = 20)
    common_txt.draw_info('Main menu (M)', pos = [300, 550], size = 30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            save_all_SB()
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            click_sound.play()
            if event.key == pg.K_m:
                A_page = False
    pg.display.update()
    screen.fill(black)
    clock.tick(fps)

def settings_page():
    global fps, bot_num, St_page, gamemode, pos_yes_icon, chaser_speed, music_on, sound_on, vol_click, vol_Kill_bot, vol_gameover
    
    if music_on == True:
        status_M = 'on'
    else:
        status_M = 'off'
    if sound_on == True:
        status_S = 'on'
    else:
        status_S = 'off'
        
    yes_icon = pg.image.load("yes_icon.png")
    yes_icon = pg.transform.smoothscale(yes_icon, (30, 30))
    screen.blit(yes_icon, pos_yes_icon)
    
    common_txt.draw_info('difficulties:', pos = [120, 200], size = 30)
    common_txt.draw_info('easy (E)   :few of boring enemies', pos = [120, 250], size = 30)
    common_txt.draw_info('normal (N) :normal numbers of normal enemies', pos = [120, 300], size = 30)
    common_txt.draw_info('hard (H)   :more of faster enemies', pos = [120, 350], size = 30)
    common_txt.draw_info('hell(I)    :large numbers of very challenging enemies', pos = [120, 400], size = 30)
    common_txt.draw_info('music (C): {M}'.format(M = status_M), pos = [150, 500], size = 25)
    common_txt.draw_info('sound (S): {S}'.format(S = status_S), pos = [150, 550], size = 25)
    common_txt.draw_info('Main menu (M)', pos = [120, 650], size = 30)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            save_all_SB()
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            click_sound.play()
            if event.key == pg.K_m:
                St_page = False
            if event.key == pg.K_e:
                bot_num = 6
                chaser_speed = 3
                gamemode = 'easy'
                pos_yes_icon = [80, 250]
            if event.key == pg.K_n:
                bot_num = 8
                chaser_speed = 4
                gamemode = 'normal'
                pos_yes_icon = [80, 300]
            if event.key == pg.K_h:
                bot_num = 12
                chaser_speed = 4.5
                gamemode = 'hard'
                pos_yes_icon = [80, 350]
            if event.key == pg.K_i:
                bot_num = 16
                chaser_speed = 5
                gamemode = 'hell'
                pos_yes_icon = [80, 400]
            if event.key == pg.K_c:
                if music_on == True:
                    music_on = False
                    pg.mixer.music.pause()
                else:
                    music_on = True
                    pg.mixer.music.unpause()
            if event.key == pg.K_s:
                if sound_on == True:
                    sound_on = False
                    vol_click = vol_Kill_bot = vol_gameover = 0
                    click_sound.set_volume(vol_click)
                    kill_bot_sound.set_volume(vol_Kill_bot)
                    gameover_sound.set_volume(vol_gameover)
                else:
                    sound_on = True
                    vol_click = 0.15
                    vol_Kill_bot = 0.35
                    vol_gameover = 0.35
                    click_sound.set_volume(vol_click)
                    kill_bot_sound.set_volume(vol_Kill_bot)
                    gameover_sound.set_volume(vol_gameover)
                
    pg.display.update()
    screen.fill(black)
    clock.tick(fps)

def score_board_page():
    global SB_page, E_SB, N_SB, H_SB, I_SB
    
    def draw_all_SB(title_size = 25, font_size = 14, space = 60):
        def draw_one_SB(SB_name, line_x, start_y, SB):
            common_txt.draw_info(SB_name, pos = [line_x, start_y], size = title_size)
            for i in range(8):
                common_txt.draw_info('{a}:{e}'.format(a=i+1, e=SB[i]), pos=[line_x, start_y+space*(i+1)], size=font_size)
        draw_one_SB('easy', 0, 10, E_SB)
        draw_one_SB('normal', scr_wid/4, 10, N_SB)
        draw_one_SB('hard', scr_wid*2/4, 10, H_SB)
        draw_one_SB('hell', scr_wid*3/4, 10, I_SB)
    
    draw_all_SB()            
    common_txt.draw_info('Main menu (M)', pos = [490, scr_hgt-150], size = 30)
    common_txt.draw_info('Clear score board (X)', pos = [0, scr_hgt-50], size = 18)
    common_txt.draw_info('Warning: ALL score data will be delated PERMANENTLY', pos = [0, scr_hgt-30], size = 18)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            save_all_SB()
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            click_sound.play()
            if event.key == pg.K_m:
                SB_page = False
            if event.key == pg.K_x:
                clear_all_SB()   
                
    pg.display.update()
    screen.fill(black)
    clock.tick(fps)

def game_run():
    global score, Gameover, MnLp
    
    while True:
        Start_page()
        
        while MnLp == True:
            main_loop()
        while A_page == True:
            Author_page()    
        while H_page == True:
            Help_page()
        while St_page == True:
            settings_page()
        while SB_page == True:
            score_board_page()
        
game_run()
