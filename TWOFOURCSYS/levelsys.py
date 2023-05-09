import xml.etree.ElementTree as ET

def readTmx(name):
   # print(f"LevelSys | Grabbing level properties from {name}...")
    tree = ET.parse(name)
    root = tree.getroot()
    lvlData=[]
    offset = 0
    err=True
    while err:
        try:
            lvlData.append(root[offset][0].text.replace("\n","").split(","))
            err=False
        except Exception:
            offset += 1
    lvlData=[]
    for i in range(6):
        try: lvlData.append(root[offset+i][0].text.replace("\n","").split(","))
        except: print(root[offset+i]," (Append has failed) | LevelSys")
    #print(f"LevelSys | Finished grabbing level data from {name}")
    return lvlData

def getProperties(name):
    tree = ET.parse(name)
    root = tree.getroot()
    lvlPropLabel = ["Game Title", "Background Color 1", "Background Color 2", "Level Title", "Loop on X?", "Loop on Y?"]
    lvlPropAttr = ["addTitle","bgCol1","bgCol2","levelTitle","loopX","loopY"]
    return {lvlPropAttr[i]: (root[0][i].get("value")) for i in range(6)}