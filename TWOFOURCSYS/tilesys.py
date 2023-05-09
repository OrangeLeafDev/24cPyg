import pygame, math, os

def imgTileSeg(png,format): # assumes png is pygame.image.load
    """_summary_

    Args:
        png (Surface): pygame.image.load
        format (int): The size of tiles

    Returns:
        list: Pygame Surfaces
    """
    pngSizeW = png.get_width()//format
    pngSizeH = png.get_height()//format
    imgTileHold = []
    print(f"TileSys | Loaded png, Resolution ({png.get_width()},{png.get_height()}), Tileset Size ({pngSizeW},{pngSizeH}), Tile Size {format}")
    for i in range(pngSizeW):
        for j in range(pngSizeH):
            image = pygame.Surface((format,format), pygame.SRCALPHA)
            image.blit(png, (0, 0), pygame.Rect(j*format,i*format,format,format))
            imgTileHold.append(image)
    print(f"TileSys | Finished setting up tileset, length of {len(imgTileHold)} (Target length {pngSizeW*pngSizeH})")
    return imgTileHold

def get_pngPiece(tileset, position=(0,0), format=16):
    """_summary_

    Args:
        tileset (dict): _description_
        position (tuple, optional): _description_. Defaults to (0,0).
        format (int, optional): _description_. Defaults to 16.
    """
    