# -*- coding: UTF-8 -*-
# 病毒大战游戏 精灵类

import random
import pygame
import globalvar as gl

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 600, 720)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建病毒的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# # 病毒落到屏幕底的个数
# virus_bottom_count = 0


class GameSprite(pygame.sprite.Sprite):
    """病毒大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):

        # 1. 调用父类方法实现精灵的创建(image/rect/speed)
        super().__init__("./res/background宽.jpg")

        # 2. 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 1. 调用父类的方法实现
        super().update()

        # 2. 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Virus(GameSprite):
    """病毒精灵"""

    def __init__(self):

        # 1. 调用父类方法，创建病毒精灵，同时指定病毒图片
        super().__init__("./res/病毒.png")

        # 2. 指定病毒的初始随机速度 1 ~ 3
        # self.speed = random.randint(1, 3)
        self.speed = 2
        self.speed_x = random.randint(-3, 3)

        # 3. 病毒水平方向移动次数
        self.x_count = 0

        # 4. 指定病毒的初始随机位置
        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

        # 5. 病毒的得分
        self.score = 5

    def update(self):

        # 1. 病毒垂直方向移动
        self.rect.y += self.speed

        # 2. 病毒水平方向移动
        self.rect.x += self.speed_x
        self.x_count += 1
        if self.x_count >= 10:
            self.speed_x = random.randint(-3, 3)
            self.x_count = 0

        # 3. 判断是否飞出屏幕，如果是，需要从精灵组删除
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # 病毒扩散数加一
            gl.add_vbc()
            print(gl.get_vbc())
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()

        # 4. 判断是否飞出屏幕两边，如果是，让病毒换个水平方向
        if self.rect.x >= SCREEN_RECT.width or self.rect.x <= 0:
            self.speed_x = -self.speed_x
            self.x_count = 0

    def __del__(self):
        # print("敌机挂了 %s" % self.rect)
        pass


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self, hero_img):

        # 1. 调用父类方法，设置image&speed
        super().__init__(hero_img, 0)

        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

        # 4. 设置英雄的速度
        self.speed_x = 0
        self.speed_y = 0

    def update(self):

        # 英雄在水平方向移动
        self.rect.x += self.speed_x

        # 英雄在垂直方向移动
        self.rect.y += self.speed_y

        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        # print("发射子弹...")

        # 1. 创建子弹精灵
        bullet = Bullet()

        # 2. 设置精灵的位置
        bullet.rect.bottom = self.rect.y
        bullet.rect.centerx = self.rect.centerx

        # 3. 将精灵添加到精灵组
        self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):

        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./res/playerbullet.png", -2)

    def update(self):

        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print("子弹被销毁...")
        pass

