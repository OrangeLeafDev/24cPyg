import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

# Cache for parsed TMX files to avoid repeated disk I/O
_tmx_cache: Dict[str, ET.Element] = {}

def readTmx(name: str) -> List[List[str]]:
    """Read and parse TMX file, returning tilemap layers with caching.
    
    Args:
        name: Path to TMX file
    
    Returns:
        List of tile layers (each layer is a list of tile strings)
    """
    # Return cached result if available
    if name in _tmx_cache:
        root = _tmx_cache[name]
    else:
        # Parse file and cache the root element
        try:
            tree = ET.parse(name)
            root = tree.getroot()
            _tmx_cache[name] = root
        except Exception as e:
            print(f"LevelSys | Failed to parse TMX '{name}': {e}")
            return []
    
    lvlData = []
    offset = 0
    
    # Find first layer with data
    err = True
    while err and offset < len(root):
        try:
            layer_data = root[offset][0].text
            if layer_data:
                lvlData.append(layer_data.replace("\n", "").split(","))
            err = False
        except (IndexError, AttributeError, TypeError):
            offset += 1
    
    # Read up to 6 layers
    for i in range(6):
        try:
            if offset + i < len(root):
                layer_data = root[offset + i][0].text
                if layer_data:
                    lvlData.append(layer_data.replace("\n", "").split(","))
        except (IndexError, AttributeError, TypeError):
            print(f"LevelSys | Warning: Could not parse layer {i} from {name}")
    
    return lvlData

def getProperties(name: str) -> Dict[str, str]:
    """Extract map properties from TMX file with caching.
    
    Args:
        name: Path to TMX file
    
    Returns:
        Dictionary of property name -> value
    """
    # Use cache if available
    if name in _tmx_cache:
        root = _tmx_cache[name]
    else:
        try:
            tree = ET.parse(name)
            root = tree.getroot()
            _tmx_cache[name] = root
        except Exception as e:
            print(f"LevelSys | Failed to parse TMX '{name}': {e}")
            return {}
    
    lvlPropLabel = ["Game Title", "Background Color 1", "Background Color 2", "Level Title", "Loop on X?", "Loop on Y?"]
    lvlPropAttr = ["addTitle", "bgCol1", "bgCol2", "levelTitle", "loopX", "loopY"]
    
    result = {}
    for i in range(len(lvlPropAttr)):
        try:
            result[lvlPropAttr[i]] = root[0][i].get("value", "")
        except (IndexError, AttributeError):
            result[lvlPropAttr[i]] = ""
            print(f"LevelSys | Warning: Missing property '{lvlPropLabel[i]}'")
    
    return result

def clear_cache() -> None:
    """Clear the TMX cache to free memory."""
    _tmx_cache.clear()
    print("LevelSys | TMX cache cleared")
