import pygame
flipInt = lambda integ, limit: (integ-limit)*-1
def generate(xBool, yBool, space, offset, col1, col2, loopInt, SCREEN_WIDTH, SCREEN_HEIGHT):
    bgSurf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for i in range(loopInt):
        flipped_I = flipInt(i,loopInt-2)
        if xBool and yBool:
            pygame.draw.rect(bgSurf,[col1, col2][flipped_I%2], pygame.Rect(SCREEN_WIDTH//2-space/2*flipped_I-offset, SCREEN_HEIGHT//2-space/2*flipped_I-offset, space*flipped_I+offset*2, space*flipped_I+offset*2))
        elif xBool:
            pygame.draw.rect(bgSurf,[col1, col2][flipped_I%2], pygame.Rect(SCREEN_WIDTH//2-space/2*flipped_I-offset, 0, space*flipped_I+offset*2, SCREEN_HEIGHT))
        elif yBool:
            pygame.draw.rect(bgSurf,[col1, col2][flipped_I%2], pygame.Rect(0, SCREEN_HEIGHT//2-space/2*flipped_I-offset, SCREEN_WIDTH, space*flipped_I+offset*2))
    return bgSurf