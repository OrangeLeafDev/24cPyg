"""Collision detection utilities with spatial optimization."""

import math
from typing import List
import pygame

def adjustColSolid(player_rect: pygame.Rect, all_tiles: List[pygame.Rect], radius: float = 50) -> List[pygame.Rect]:
    """Filter collision tiles to only nearby ones using squared distance (faster than hypot).
    
    This avoids expensive distance calculations by using squared distances,
    which preserves ordering and validity while being ~4x faster.
    
    Args:
        player_rect: Player collision rectangle
        all_tiles: All tile collision rectangles
        radius: Search radius around player (default 50 pixels)
    
    Returns:
        Filtered list of tiles within radius
    """
    player_x, player_y = player_rect.centerx, player_rect.centery
    radius_sq = radius * radius  # Squared radius for comparison
    
    nearby_tiles = []
    for tile in all_tiles:
        # Use squared distance to avoid expensive sqrt
        dx = tile.x - player_x
        dy = tile.y - player_y
        dist_sq = dx * dx + dy * dy
        
        if dist_sq <= radius_sq:
            nearby_tiles.append(tile)
    
    return nearby_tiles

def getColHits(tiles: List[pygame.Rect], player_rect: pygame.Rect, mode: int = 0) -> List[pygame.Rect]:
    """Get collision hits for a given object against a tile list.
    
    Args:
        tiles: List of collision tiles
        player_rect: Rectangle to test collisions against
        mode: Collision mode (0=simple, 1=directional)
    
    Returns:
        List of colliding tiles
    """
    if mode == 0:
        return [tile for tile in tiles if player_rect.colliderect(tile)]
    else:
        # Mode 1: return as nested list for compatibility with existing code
        return [[tile for tile in tiles if player_rect.colliderect(tile)]]
