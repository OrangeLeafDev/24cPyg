if __name__ == '__main__':
    import filesys
else:
    from TWOFOURCSYS import filesys
def readScript(file, mainDir):
    stri = filesys.readFile(f"{mainDir}/WORLDS/mainWorld/{file}")
    stri = stri.split("\n")
    sequenceQueue = {"dialog":[], "misc":[]}
    for line in stri:
        lineSyntax = line.split(" ")
        if 1:
            if lineSyntax[0] == "say":
                sequenceQueue["dialog"].append([stri.index(line),"T",' '.join(lineSyntax[1:])])
            if lineSyntax[0] == "reply":
                sequenceQueue["dialog"].append([stri.index(line),"P",' '.join(lineSyntax[1:])])
            if lineSyntax[0] == "shake":
                sequenceQueue["misc"].append([stri.index(line),"SHK"])
            if lineSyntax[0] == "music":
                sequenceQueue["misc"].append([stri.index(line),"MSC",' '.join(lineSyntax[1:])])
            if lineSyntax[0] == "destroy":
                sequenceQueue["misc"].append([stri.index(line),"DEST",' '.join(lineSyntax[1:])])
            if lineSyntax[0] == "trinkVerify":
                sequenceQueue["misc"].append([stri.index(line),"TRINK",' '.join(lineSyntax[1:])])
    sequenceQueue["len"] = sum(len(value) for key, value in sequenceQueue.items())
    return sequenceQueue