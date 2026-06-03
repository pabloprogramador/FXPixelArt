from PIL import Image
import numpy as np

width, height = 32, 8

# Criar imagem com canal alfa (RGBA)
img = np.zeros((height, width, 4), dtype=np.uint8)

def make_transparent_positions(width, base):
    positions = set()
    x = base
    while x < width - base:
        positions.add(x)
        remaining = (width - base) - x
        gap = max(1, round(base * remaining / (width - 2 * base)))
        x += gap + 1
    for x in range(width - base, width):
        positions.add(x)
    return positions

# Padrões separados: base=5 para vermelhas (linhas pares), base=7 para amarelas (linhas ímpares)
transparent_positions_red = make_transparent_positions(width, 5)
transparent_positions_yellow = make_transparent_positions(width, 7)

for y in range(height):
    for x in range(width):
        # Escolher cor conforme paridade da linha: par = vermelho, impar = amarelo
        if y % 2 == 0:
            r, g, b = 255, 0, 0
            transparent_positions = transparent_positions_red
        else:
            r, g, b = 255, 0, 0
            transparent_positions = transparent_positions_yellow

        a = 0 if x in transparent_positions else 255
        img[y, x] = [r, g, b, a]

Image.fromarray(img, "RGBA").save("pixel.png")