"""
    @file        main_example.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Basic example for creating symbols from an image
    @version     1.0
    @date        2024-04-20
    
"""
# Includes
from symbol_manager_ili9431 import *

# Works only with binary images!
# Works better with images proportional to col_size*row_size 

# Letter A example 
# Enter below an image path and the symbols' dimensions to display it and for printing the hexadecimal list for copy-pasting:
img_path = r"img\\letterA.png"
col_size = 32
row_size = 52

# Processing
patches = patchify(img_path, col_size, row_size)
binTab = reconstructBinTab(patches, col_size, row_size)
hexTab = hexMatrix(binTab, col_size)

# Displaying
displaySymbol(hexTab, row_size)
copyPasteSymbolPrint(hexTab)


