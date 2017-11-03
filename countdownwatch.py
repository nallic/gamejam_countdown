import cv2
import numpy as np
from datetime import datetime, time
import sys, pygame
#import matplotlib.pyplot as plt

''' configuration '''

deadline = datetime(day=18, month=10, year=2017, hour=22, minute=00)
print ('deadline is : ' + str(deadline))

size = width, height = 640, 480

''' constants '''

black = (0, 0, 0)
white = (255,255,255)

''' program '''
pygame.init()

clock = pygame.time.Clock()
pygame.key.set_repeat(500, 50)

#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
font = pygame.font.Font('LCD.ttf', 170)
cursor = [[0, 0], [width, 0], [0, height], [width, height]]
cursor_idx = 0
cursor_on = False

first_run = True

def save_settings():
    print("saving")
    pass # todo Implement

def load_settings():
    print("loading")
    pass # todo Implement

''' Find the smallest size of a box containing the 4 corners 
    (topleft, topright, botleft, botright) (flipping not supported)
'''
def find_corner_rectsize(cursors):
    height = max(cursors[3][1], cursors[2][1]) - min(cursors[0][1], cursors[1][1])
    width = max(cursors[3][0], cursors[1][0]) - min(cursors[0][0], cursors[2][0])

    return (width, height)

while 1:
    clock.tick(60) # 30 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE: sys.exit()

            if cursor_on:
                if event.key == pygame.K_LEFT:
                    cursor[cursor_idx][0] -= 1;
                if event.key == pygame.K_RIGHT:
                    cursor[cursor_idx][0] += 1;
                if event.key == pygame.K_UP:
                    cursor[cursor_idx][1] -= 1;
                if event.key == pygame.K_DOWN:
                    cursor[cursor_idx][1] += 1;
                if event.key == pygame.K_SPACE:
                    cursor_idx = (cursor_idx + 1) % 4;

            if event.key == pygame.K_RETURN and not first_run:
                cursor_on = not cursor_on;
            if event.key == pygame.K_s:
                save_settings()
            if event.key == pygame.K_l:
                load_settings()

    current_timer_s = (deadline - datetime.now()).seconds
    current_timer_hours = current_timer_s // 3600
    # remaining seconds
    current_timer_s = current_timer_s - (current_timer_hours * 3600)
    # minutes
    current_timer_minutes = current_timer_s // 60
    # remaining seconds
    current_timer_s = current_timer_s - (current_timer_minutes * 60)

    current_timer_string = '%02d:%02d:%02d' % (current_timer_hours, current_timer_minutes, current_timer_s)
    current_timer = font.render(current_timer_string, True, white, black)

    cv_current_timer = pygame.surfarray.array3d(current_timer)
    cv_current_timer = np.flipud(np.rot90(cv_current_timer))

    # plt.imshow(cv_current_timer)
    # plt.show()

    cols, rows  = current_timer.get_size()

    if first_run: cursor = [[0, 0], [cols, 0], [0, rows], [cols, rows]]

    pts1 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
    pts2 = np.float32(cursor)
    M = cv2.getPerspectiveTransform(pts1, pts2)

    cv_current_timer = cv2.warpPerspective(cv_current_timer, M, find_corner_rectsize(cursor))

    cv_current_timer = np.rot90(np.flipud(cv_current_timer),-1)
    current_timer = pygame.surfarray.make_surface(cv_current_timer)

    screen.fill(black)
    timer_on_display = screen.blit(current_timer, (0, 0))
    cur_cursor_offset = (cursor[cursor_idx][0] + timer_on_display.topleft[0], cursor[cursor_idx][1] + timer_on_display.topleft[1])
    if cursor_on: pygame.draw.circle(screen, (255, 0, 0), cur_cursor_offset, 3, 0)
    pygame.display.flip()

    # Not first run any more
    first_run = False



