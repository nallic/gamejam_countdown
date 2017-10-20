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

screen = pygame.display.set_mode(size)
font = pygame.font.Font('digital-7.mono.ttf', 150)

while 1:
    clock.tick(30) # 30 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

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
    #plt.imshow(cv_current_timer)
    #plt.show()

    cols, rows  = current_timer.get_size()
    pts1 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
    pts2 = np.float32([[0, 0], [cols, 0], [0+40, rows], [cols-40, rows+20]])
    M = cv2.getPerspectiveTransform(pts1, pts2)

    cv_current_timer = cv2.warpPerspective(cv_current_timer, M, (cols, rows+20))

    cv_current_timer = np.rot90(np.flipud(cv_current_timer),-1)
    current_timer = pygame.surfarray.make_surface(cv_current_timer)

    screen.fill(black)
    screen.blit(current_timer, current_timer.get_rect(center=(width/2, height/2)))
    pygame.display.flip()





