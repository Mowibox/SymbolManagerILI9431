"""
    @file        symbol_manager_ili9431.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Allows to display or create symbols for the TFT screen ILI9431
    @version     1.0
    @date        2024-04-20
    
"""

# Includes
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Functions
def binMatrix(hexTab: list, row_size: int) -> list:
    """
    Converts the hexadecimal list passed as a parameter into its binary representation. The digits are concatenated according to the row size.

    @param hexTab: List of hexadecimal characters
    @param row_size: Number of rows in the symbol
    """
    assert 2*row_size == len(hexTab)
    binTab = []
    for i in range(0, (2*row_size)-1, 2):
        row = format(hexTab[i], '016b') + format(hexTab[i+1], '016b')
        binTab.append(row)

    return binTab


def displaySymbol(hexTab: list, row_size: list) -> any:
    """
    Display the symbol from the hexadecimal list passed as a parameter

    @param hexTab: List of hexadecimal characters
    @param row_size: Number of rows in the symbol
    """
    binTab = binMatrix(hexTab, row_size)
    img = [[int(bit) for bit in row] for row in binTab]
    plt.imshow(img, cmap='binary')
    return plt.show()


def patchify(img_path: str, col_size: int, row_size: int) -> list:
    """
    Divides an image of size h*w into blocks of size h//row_size w//col_size. The resulting patches are averaged to return 1 or 0.

    @param img_path: Path to the image
    @param col_size: Number of columns in the symbol
    @param row_size: Number of rows in the symbol
    """
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    h, w = image.shape

    patch_height = h//row_size
    patch_width = w//col_size

    patches = []
    for row in range(row_size):
        for col in range(col_size):
            y_start = row * patch_height
            y_end = (row + 1) * patch_height
            x_start = col * patch_width
            x_end = (col + 1) * patch_width

            patch = image[y_start:y_end, x_start:x_end]

            mean_value = np.mean(patch)
            binary_value = 0 if mean_value > 128 else 1
            patches.append(binary_value)

    return patches


def reconstructBinTab(patches: list, col_size: int, row_size: int) -> list:
    """
    Reconstructs the binary list based on the input patches.

    @param patches: Binary list of patches
    @param col_size: Number of columns in the symbol
    @param row_size: Number of rows in the symbol
    """
    binTab = []
    for j in range(row_size):
        binVal = ''
        for i in range(col_size):
            binVal += str(patches[i+j*col_size])
        binTab.append(binVal)
    return binTab


def hexMatrix(binTab: list, col_size: int) -> list:
    """
    Converts a binary list into its hexadecimal representation. The digits are split according to the column size.

    @param binTab: List of binary characters
    @param col_size: Number of columns in the symbol
    """
    hexTab = []
    for row in binTab:
        hexVal1 = int(row[:col_size//2], 2)
        hexVal2 = int(row[col_size//2:], 2)
        hexTab.extend([hexVal1, hexVal2])
    return hexTab


def imgToSymbol(img_path: str, col_size: int, row_size: int) -> list:
    """
    Converts an image into its hexadecimal representation.

    @param img_path: Path to the image
    @param col_size: Number of columns in the symbol
    @param row_size: Number of rows in the symbol
    """
    patches = patchify(img_path, col_size, row_size)
    binTab = reconstructBinTab(patches, col_size, row_size)
    hexTab = hexMatrix(binTab, row_size)
    return hexTab


def copyPasteSymbolPrint(hexTab: list) -> any:
    """
    Returns hexadecimal characters in the format 0x without spaces. This allows for easier copy-pasting.

    @param hexTab: List of hexadecimal characters
    """
    symbol = [f'0x{i:04X}' for i in hexTab]
    symbol = str(symbol).replace("'", "")
    symbol = symbol.replace(" ", "")
    symbol = symbol.replace("[", "")
    symbol = symbol.replace("]", "")
    return print(symbol)
