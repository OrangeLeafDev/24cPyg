def writeFile(name,data):
    with open(name, 'w', encoding="utf8") as f:
        f.write(data)
    #print(f"FileSys | Finished writing data to {name}")

def readFile(name):
    #print(f"FileSys | Finished grabbing data from {name}")
    with open(name, encoding="utf8") as f:
        return f.read()
    
