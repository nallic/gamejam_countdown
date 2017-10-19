import cv2
import numpy as np
from datetime import datetime, time
import sys, pygame
#import matplotlib.pyplot as plt

''' configuration '''

deadline = datetime(day=18, month=10, year=2017, hour=22, minute=00)
print ('deadline is : ' + str(deadline) + ' which is ' + str((deadline - datetime.now()).seconds/3600) + ' hours from now')

size = width, height = 640, 480

''' constants '''

black = (0, 0, 0)
white = (255,255,255)

''' helpers '''

def surface_to_string(surface):
    """Convert a pygame surface into string"""
    return pygame.image.tostring(surface, 'RGB')


def pygame_to_cvimage(surface):
    """Convert a pygame surface into a cv image"""
    cv_image = cv2.CreateImageHeader(surface.get_size(), cv2.IPL_DEPTH_8U, 3)
    image_string = surface_to_string(surface)
    cv2.SetData(cv_image, image_string)
    return cv_image


def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    image_rgb = cv2.CreateMat(image.height, image.width, cv2.CV_8UC3)
    cv2.CvtColor(image, image_rgb, cv2.CV_BGR2RGB)
    return pygame.image.frombuffer(image.tostring(), cv2.GetSize(image_rgb),
                                   "RGB")

''' program '''
pygame.init()

screen = pygame.display.set_mode(size)
font = pygame.font.Font('digital-7.mono.ttf', 150)

while 1:
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

    current_timer = font.render(current_timer_string, False, white, black)

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





