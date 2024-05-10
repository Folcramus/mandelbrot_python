import pygame
import os
from functools import lru_cache
import pygame.camera
from pygame import Surface
from pygame.locals import *
from numba import njit, prange
from pygame_widgets.button import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ----------  чтобы окно появлялось в верхнем левом углу ------------
x = 20
y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
# --------------------------------------------------------------------


pygame.init()
W = 600
H = 600

pygame.display.set_caption("Множество Мандельброта")

FPS = 120  # число кадров в секунду
clock = pygame.time.Clock()

P = 300  # размер [2*P+1 x 2*P+1]
scale = P / 2  # масштабный коэффициент
view = [0, 0]  # координаты смещения угла обзора
n_iter = 100  # число итераций для проверки принадлежности к множеству Мандельброта
booling = True

sc = pygame.display.set_mode((W, H))
sc.fill(WHITE)


@njit(fastmath=True)
def calcig(z, c):
    k = 0
    for n in prange(n_iter):
        k = n
        z = z ** 4 + c
        if abs(z) > 2:
            return k
    return k


def mandelbrot(P, scale, view, n_iter):
    for y in prange(-P + view[1], P + view[1]):
        for x in prange(-P + view[0], P + view[0]):
            a = x / scale
            b = y / scale
            c = complex(a, b)
            z = complex(0)
            n = calcig(z, c)

            if n == n_iter - 1:
                r = g = b = 0
            else:
                r = (n % 2) * 32 + 128
                g = (n % 4) * 64
                b = (n % 2) * 16 + 128

            pygame.draw.circle(sc, (r, g, b), (x + P - view[0], y + P - view[1]), 1)


if booling:
    mandelbrot(P, scale, view, n_iter)
    booling = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                scale += 20
            if event.y == -1:
                scale -= 20
            mandelbrot(P, scale, view, n_iter)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                pygame.image.save(sc, 'abc.jpg')
            if event.key == pygame.K_a:
                view[0] += 10
            if event.key == pygame.K_d:
                view[0] -= 10
            if event.key == pygame.K_w:
                view[1] += 10
            if event.key == pygame.K_s:
                view[1] -= 10
            mandelbrot(P, scale, view, n_iter)
    pygame.display.update()
    clock.tick(FPS)
