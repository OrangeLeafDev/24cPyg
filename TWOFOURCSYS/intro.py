import pygame, math, os
pygame.init()
def main(screen, mainDir):  # sourcery skip: low-code-quality
    flipNum = lambda num, range: num*-1+range
    if "ANDROID_BOOTLOGO" in os.environ:
        notAndroidCheck = False
        pygame.display.set_caption("24Colors - Pathetic Android User.")
    else:
        notAndroidCheck = True
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    centerX = SCREEN_WIDTH//2
    centerY = SCREEN_HEIGHT//2
    print(mainDir)
    black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    black.fill((0, 0, 0))
    logo = pygame.image.load(
        f"{mainDir}//orangeleafdev.png"
    ).convert_alpha()
    logo = pygame.transform.scale(logo, (100,100))
    regularFont = pygame.font.Font(f"{mainDir}//FONT//pixel-insanity-consolas.ttf",32)
    smallFont = pygame.font.Font(f"{mainDir}//FONT//pixel-insanity-consolas.ttf",24)
    textimg = [
        [logo, pygame.Vector2(centerX-100,centerY-45), pygame.Vector2(centerX, centerY), (255, 255, 0)],
        [regularFont.render("Or",False,(255, 125, 0),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("an",False,(255, 125, 0),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("ge",False,(255, 125, 0),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("Le",False,(50, 255, 0),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("af",False,(50, 255, 0),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("36",False,(255, 0, 255),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("/",False,(255, 255, 255),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("Dev",False,(255, 0, 0),(0,0,0)), pygame.Vector2(centerX,centerY), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [regularFont.render("24Colors",False,(125, 125, 125),(0,0,0)), pygame.Vector2(centerX,centerY*1.25), pygame.Vector2(centerX, SCREEN_HEIGHT)],
        [smallFont.render("Made by:",False,(200, 200, 200),(0,0,0)), pygame.Vector2(centerX,centerY*3/4), pygame.Vector2(centerX, -32)]
    ]
    if not notAndroidCheck: textimg[9][0] = regularFont.render("24Colors - You better have a keyboard...",False,(125, 125, 125),(0,0,0))
    opac = 0
    timer = 0
    timer2 = 1
    while timer < timer2+1 and opac < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN] and notAndroidCheck:
                timer = 2
            elif event.type in [pygame.KEYDOWN] and not notAndroidCheck:
                textimg[9][0] = regularFont.render("24Colors - You do!",False,(125, 125, 125),(0,0,0))
                notAndroidCheck = True
            elif event.type in [pygame.FINGERDOWN] and not notAndroidCheck:
                textimg[9][0] = regularFont.render("24Colors - Nope, no fingers.",False,(125, 125, 125),(0,0,0))
        screen.fill((0,0,0))
        deltaTime = pygame.time.Clock().tick(120)/1000
        timer += deltaTime
        if not notAndroidCheck: timer2 += deltaTime
        textOffset = 0
        black.set_alpha(opac)
        for i in textimg:
            if textimg.index(i)*0.09 < timer:
                if textimg.index(i) >= 9:
                    i[2] += (-i[2]+i[1])/24* deltaTime*120
                    i[0].set_alpha(flipNum(math.dist(i[2],i[1]), 255))
                else:
                    i[2] += (-i[2]+i[1]+pygame.Vector2(textOffset-110,0))/24* deltaTime*120
                    i[0].set_alpha(flipNum(math.dist(i[2],i[1]+pygame.Vector2(textOffset-110,0)), 255))
            if textimg.index(i) == 0:
                screen.blit(i[0],i[2])
            else:
                screen.blit(i[0],i[2] if textimg.index(i) <= 8 else i[2]-(i[0].get_width()//2,0))
                textOffset += i[0].get_width()
        if timer > timer2 and notAndroidCheck:
            screen.blit(black, (0,0))
            opac += 2.5
        pygame.display.update()
    return 1
