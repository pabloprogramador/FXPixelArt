from PIL import Image
import numpy as np

# =========================
# FUNÇÃO PARA GERAR BAYER NxN
# =========================

def generate_bayer(n):

    if n == 2:
        return np.array([
            [0, 2],
            [3, 1]
        ])

    smaller = generate_bayer(n // 2)

    top_left = 4 * smaller + 0
    top_right = 4 * smaller + 2
    bottom_left = 4 * smaller + 3
    bottom_right = 4 * smaller + 1

    top = np.hstack((top_left, top_right))
    bottom = np.hstack((bottom_left, bottom_right))

    matrix = np.vstack((top, bottom))

    return matrix


# =========================
# MATRIZES
# =========================

BAYER_2X2 = generate_bayer(2) / 4
BAYER_4X4 = generate_bayer(4) / 16
BAYER_8X8 = generate_bayer(8) / 64
BAYER_16X16 = generate_bayer(16) / 256


# =========================
# ESCOLHER MATRIZ
# =========================

def get_bayer(choice):

    if choice == "a":
        return BAYER_2X2

    elif choice == "b":
        return BAYER_4X4

    elif choice == "c":
        return BAYER_8X8

    elif choice == "d":
        return BAYER_16X16

    else:
        print("Opção inválida. Usando 8x8.")
        return BAYER_8X8


# =========================
# GERAR GRADIENT
# =========================

def generate_gradient(width, bayer_matrix):

    matrix_size = bayer_matrix.shape[0]

    # altura proporcional
    # height = width // 8
    height = 8

    # gradient horizontal
    gradient = np.tile(
        np.linspace(0, 255, width, dtype=np.float32),
        (height, 1)
    )

    # repetir matriz Bayer
    tiled_bayer = np.tile(
        bayer_matrix,
        (
            height // matrix_size + 1,
            width // matrix_size + 1
        )
    )[:height, :width]

    # ordered dithering
    normalized = gradient / 255.0
    dithered = (normalized > tiled_bayer).astype(np.uint8) * 255

    # =========================
    # RGBA
    # branco = transparente
    # preto = visível
    # =========================

    rgba = np.zeros((height, width, 4), dtype=np.uint8)

    rgba[dithered == 0] = [0, 0, 0, 255]

    rgba[dithered == 255] = [255, 255, 255, 0]

    return Image.fromarray(rgba, mode="RGBA")


# =========================
# INPUTS
# =========================

width = int(input("Digite a largura: "))

print("\nEscolha a matriz Bayer:")
print("a - 2x2")
print("b - 4x4")
print("c - 8x8")
print("d - 16x16")

choice = input("\nOpção: ").lower()

bayer = get_bayer(choice)

# =========================
# GERAR IMAGEM
# =========================

img = generate_gradient(width, bayer)

img.save("gradient_transparente.png")

print("\nImagem salva como:")
print("gradient_transparente.png")