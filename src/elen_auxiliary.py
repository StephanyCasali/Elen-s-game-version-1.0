import pygame
import math
import elen_class as ec

def get_images(image_path: str, x: tuple):
    elen = pygame.image.load(image_path)
    elen = pygame.transform.scale(elen, x)
    return elen

def position_is_free(x: int, y: int, objects: list[ec.Entity], obj_width: int, obj_height: int) -> bool:
    new_rect = pygame.Rect(x, y, obj_width, obj_height)
    for obj in objects:
        obj_rect = pygame.Rect(obj.x, obj.y, obj_width, obj_height)
        if new_rect.colliderect(obj_rect):
            return False
    return True

def check_collision_circle(entity1: ec.Entity, entity2: ec.Entity, radius1: int, radius2: int):
    distance = math.sqrt((entity1.x - entity2.x) ** 2 + (entity1.y - entity2.y) ** 2)
    return distance <= (radius1 + radius2)

def check_collision(entity1: ec.Entity, size1:tuple, entity2:ec.Entity, size2:tuple) -> bool:
    player_rect = pygame.Rect(entity1.x, entity1.y, size1[0], size1[1])
    key_rect = pygame.Rect(entity2.x, entity2.y, size2[0], size2[1])
    if player_rect.colliderect(key_rect):
        return True
    return False