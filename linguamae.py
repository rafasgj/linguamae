#!/usr/bin/env python3
"""
Lingua Mae.

    Obra audiovisual de Camila Proto.
    Codificacao Rafael Jeffman.
"""

import sys
import pygame
from pygame.locals import (FULLSCREEN, KMOD_LALT, KMOD_CAPS, KMOD_LSHIFT,
                           KMOD_LCTRL, K_ESCAPE, QUIT, MOUSEBUTTONDOWN,
                           KEYDOWN)
from random import random
from string import ascii_letters


# initialize
pygame.init()

# constants
partial = (p.lower() for p in ('FOI', 'RAFASGJ', 'RAFASGJ CLOSE'))
quit_text = 'rafasgj close it'.lower()

min_x, min_y = 50, 50

# load font, prepare values
fontfile = pygame.font.match_font('arial')
font = pygame.font.Font(fontfile, 80)


def clear_screen():
    """Clear screen."""
    global font, next_letter, max_y
    next_letter = (min_x, min_y)
    # fill background
    screen.fill(wincolor)
    # Render title
    # text = 'Língua Mãe'
    # text_width, text_height = font.size(text)
    # ren = font.render(text, 1, fg, bg)
    # max_y = int(height * 0.8) - text_height - 60
    # screen.blit(ren, (width - text_width - 10, max_y + 70))
    pygame.display.flip()


def render_letter(key):
    """Render a letter on the screen."""
    global next_letter
    if next_letter[1] > height*0.6:
        clear_screen()
    text_width, text_height = font.size(key)
    ren = font.render(key, 1, fg, bg)
    screen.blit(ren, next_letter)
    x, y = next_letter[0] + text_width, next_letter[1]
    if x > width * 0.6:
        x, y = min_x, next_letter[1] + text_height
    next_letter = (x, y)
    pygame.display.flip()
    if key != ' ':
        play_letter(key)


def play_letter(key):
    """Play audio for a single letter."""
    # audios
    limit = (60, 59, 61, 60, 60, 62, 61, 60, 60, 60,
             0, 61, 60, 60, 60, 60, 60, 61, 60, 60,
             60, 60, 0, 0, 0, 0)
    # letter index
    index = ord(key)-ord('a')
    count = limit[index]
    if count > 0:
        play_audio("{0}-{1:03}".format(key, int(random() * count)))


def play_audio(filename):
    """Play an audio file."""
    pygame.mixer.Sound('audio/' + filename + ".ogg").play()


# start screen
modes = pygame.display.list_modes()
width, height = modes[0]
flags = FULLSCREEN if '-w' not in sys.argv else 0
screen = pygame.display.set_mode(modes[0], flags, 16)

QUIT_MODE = (KMOD_LSHIFT | KMOD_LCTRL | KMOD_LALT | KMOD_CAPS)

fg = 240, 240, 230
bg = 0, 0, 0
wincolor = 0, 0, 0

clear_screen()
word = ''
while True:
    # use event.wait to keep from polling 100% cpu
    evt = pygame.event.wait()
    if evt.type in (QUIT,):
        break
    elif evt.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if evt.key == K_ESCAPE and mods == QUIT_MODE:
            break
        k = chr(evt.key).lower()
        if k == ' ' and word not in partial:
            word = ''
        else:
            word += k

        if k in ascii_letters or k == ' ':
            render_letter(k)

        if word == quit_text:
            print("should've closed")
            break
        # elif word == 'BRASIL'.lower():
        #     play_audio("Fora_Temer")
        # elif word == 'FOI GOLPE'.lower():
        #     play_audio("Solucao_Michel")

pygame.quit()
