# -*- coding: UTF-8 -*-
# 全局变量管理器


def _init():
    # 病毒落到屏幕底的个数
    global virus_bottom_count
    virus_bottom_count = 0


def add_vbc():
    global virus_bottom_count
    virus_bottom_count += 1


def get_vbc():
    return virus_bottom_count
