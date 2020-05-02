# -*- coding: UTF-8 -*-
# 病毒大战游戏主类

import pygame
from virus_sprites import *
from sys import exit
from pygame.locals import *
import globalvar as gl


class VirusGame(object):
    """病毒大战主游戏"""

    def __init__(self):

        pygame.init()
        print("游戏初始化")

        # 1. 创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 设置窗口标题
        pygame.display.set_caption("病毒大战")
        # 加载背景音乐
        pygame.mixer.music.load("./res/the phoenix.mp3")
        # 播放背景音乐，-1表示循环播放
        pygame.mixer.music.play(-1)

        # 1/0表示玩家有/无生命
        self.player1 = 1
        self.player2 = 0

        # 玩家的分数
        self.player1_score = 0
        self.player2_score = 0

        # self.create_sprites()

        # 4. 设置定时器事件 - 创建病毒　1s
        # 5. 英雄发射子弹事件 - 创建子弹 0.5s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def game_welcome(self):

        # 创建背景
        bg = Background()
        self.screen.blit(bg.image, (0, 0))
        # 颜色列表 [红，白，白]
        color_list = [(255, 0, 0), (255, 255, 255)]
        # 选项
        item = 0
        waiting = True
        while waiting:
            self.clock.tick(10)
            # 绘制文字
            self.drawText(text="单人游戏", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2, fontColor=color_list[0])
            self.drawText(text="双人游戏", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2 + 80,
                          fontColor=color_list[1])
            self.drawText(text="按Enter键开始游戏", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height - 50, textHeight=20,
                          fontColor=(80, 150, 80))
            # 更新屏幕
            pygame.display.update()
            key_pressed = pygame.key.get_pressed()
            # 处理键盘事件 （换个颜色）
            if key_pressed[K_UP] or key_pressed[K_DOWN]:
                color_3 = color_list[0]
                color_list[0] = color_list[1]
                color_list[1] = color_3
                item = (item + 1) % 2
            # 按回车开始游戏(键值为13)
            if key_pressed[13]:
                waiting = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        return item

    def drawText(self, text, posx, posy, textHeight=48, fontColor=(255, 0, 0)):
        fontObj = pygame.font.Font('./res/STHUPO.TTF', textHeight)  # 通过字体文件获得字体对象
        textSurfaceObj = fontObj.render(text, True, fontColor)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        textRectObj.center = (posx, posy)  # 设置显示对象的坐标
        self.screen.blit(textSurfaceObj, textRectObj)  # 绘制字

    def create_sprites(self, item):

        if item:
            self.player2 = 1

        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建病毒的精灵组
        self.virus_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组,玩家1和玩家2
        self.hero = Hero("./res/player.png")
        if self.player2:
            self.hero2 = Hero("./res/player2.png")
            self.hero_group = pygame.sprite.Group(self.hero, self.hero2)
        else:
            self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始...")

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            is_over = self.__check_collide()
            if is_over != 0:
                return is_over
            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():

            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("病毒出场...")
                # 创建病毒精灵
                virus = Virus()

                # 将病毒精灵添加到病毒精灵组
                self.virus_group.add(virus)
            elif event.type == HERO_FIRE_EVENT:
                if self.player1:
                    self.hero.fire()
                if self.player2:
                    self.hero2.fire()

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed_x = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed_x = -2
        else:
            self.hero.speed_x = 0

        if keys_pressed[pygame.K_DOWN]:
            self.hero.speed_y = 2
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed_y = -2
        else:
            self.hero.speed_y = 0

        if self.player2:
            if keys_pressed[pygame.K_d]:
                self.hero2.speed_x = 2
            elif keys_pressed[pygame.K_a]:
                self.hero2.speed_x = -2
            else:
                self.hero2.speed_x = 0

            if keys_pressed[pygame.K_s]:
                self.hero2.speed_y = 2
            elif keys_pressed[pygame.K_w]:
                self.hero2.speed_y = -2
            else:
                self.hero2.speed_y = 0

    def __check_collide(self):

        # 1. 子弹消灭病毒
        collide1 = pygame.sprite.groupcollide(self.hero.bullets, self.virus_group, True, True)
        if collide1:
            self.player1_score += 1
        if self.player2:
            collide2 = pygame.sprite.groupcollide(self.hero2.bullets, self.virus_group, True, True)
            if collide2:
                self.player2_score += 1

        # 2. 病毒碰到英雄
        if self.player1:
            enemies = pygame.sprite.spritecollide(self.hero, self.virus_group, True)
            if enemies:
                # 让英雄牺牲
                self.hero.kill()
                print("玩家1死亡")
                self.player1 = 0
        if self.player2:
            enemies2 = pygame.sprite.spritecollide(self.hero2, self.virus_group, True)
            if enemies2:
                # 让英雄牺牲
                self.hero2.kill()
                print("玩家2死亡")
                self.player2 = 0

        # 当病毒落底10个或玩家1和玩家2都死亡时 结束游戏
        if gl.get_vbc() >= 10:
            print("病毒已扩散，游戏失败")
            return 1
        elif self.player1 == 0 and self.player2 == 0:
            print("玩家全部死亡，游戏失败")
            return 2
        elif self.player1_score >= 100 or self.player2_score >= 100:
            print("成功消灭了病毒，游戏胜利")
            return 3
        else:
            return 0

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.virus_group.update()
        self.virus_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        if self.player2:
            self.hero2.bullets.update()
            self.hero2.bullets.draw(self.screen)

        self.drawText(text="1P SCORE:", posx=50, posy=30, textHeight=20, fontColor=(255, 255, 255))
        self.drawText(text=str(self.player1_score), posx=30, posy=50, textHeight=20, fontColor=(255, 255, 255))

        self.drawText(text="2P SCORE:", posx=550, posy=30, textHeight=20, fontColor=(255, 255, 255))
        self.drawText(text=str(self.player2_score), posx=560, posy=50, textHeight=20, fontColor=(255, 255, 255))

    def game_over(self, item3):

        # 创建背景
        bg = Background()
        self.screen.blit(bg.image, (0, 0))
        # 颜色列表 [红，白，蓝]
        color_list = [(255, 0, 0), (255, 255, 255), (0, 0, 255)]
        # 选项
        item2 = 0
        waiting = True
        while waiting:
            self.clock.tick(10)
            # 绘制文字
            if item3 == 1 or item3 == 2:
                self.drawText(text="GAME OVER", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2 - 200,
                              textHeight=100, fontColor=(0, 0, 0))
            else:
                self.drawText(text="GAME WIN", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2 - 200,
                              textHeight=100, fontColor=(0, 0, 255))
            if item3 == 1:
                self.drawText(text="病毒已扩散！注意不要让病毒落底！", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2 - 80,
                              textHeight=40, fontColor=(100, 100, 100))
            elif item3 == 2:
                self.drawText(text="玩家全部死亡！注意走位！", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2 - 80,
                              textHeight=40, fontColor=(100, 100, 100))
            self.drawText(text="再来一局", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2, fontColor=color_list[0])
            self.drawText(text="退出游戏", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height / 2 + 80,
                          fontColor=color_list[1])
            self.drawText(text="按Enter键确认", posx=SCREEN_RECT.width / 2, posy=SCREEN_RECT.height - 50, textHeight=20,
                          fontColor=(80, 150, 80))
            # 更新屏幕
            pygame.display.update()
            key_pressed = pygame.key.get_pressed()
            # 处理键盘事件 （换个颜色）
            if key_pressed[K_UP] or key_pressed[K_DOWN]:
                color_3 = color_list[0]
                color_list[0] = color_list[1]
                color_list[1] = color_3
                item2 = (item2 + 1) % 2
            # 按回车开始游戏(键值为13)
            if key_pressed[13]:
                waiting = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        return item2


if __name__ == '__main__':

    while True:
        # 初始化全局变量
        gl._init()
        # 创建游戏对象
        game = VirusGame()
        # 调用游戏加载界面方法,并判断是双人游戏还是单人游戏
        item = game.game_welcome()
        # 创建精灵和精灵组
        game.create_sprites(item)
        # 开始游戏
        item3 = game.start_game()
        # 结束游戏
        item2 = game.game_over(item3)
        if item2:
            break

    pygame.quit()
    exit()
