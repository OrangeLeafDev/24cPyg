import xml.etree.ElementTree as ET
from tkinter import filedialog as fd
import pytmx
a = fd.askopenfilename(title="Open 24c Level (.tmx or .xml)")
tree = ET.parse(a)
root = tree.getroot()
print(root,"-- Main Tree")
input("pytmx")
print(pytmx.TiledMap(a))