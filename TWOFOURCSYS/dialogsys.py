import pygame
pygame.init()
def sort(scriptDict):  # sourcery skip: low-code-quality
    scriptQueue = []
    for items in list(scriptDict.keys())[:-1]:
        print(items, scriptDict[items])
        scriptQueue.extend(iter(scriptDict[items]))
    return sorted(scriptQueue, key=lambda x: x[0])
        