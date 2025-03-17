import numpy as np
import pywt
import cv2

def embed_message(image_path, message, output_path):
    """
    Embeds a message into an image using DWT.
    """
    # Read image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Error loading image.")

    # Perform DWT
    coeffs2 = pywt.dwt2(image, 'haar')
    LL, (LH, HL, HH) = coeffs2

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message + '\0')  # Null terminator

    # Flatten LH coefficients for embedding
    LH_flat = LH.flatten()
    if len(binary_message) > len(LH_flat):
        raise ValueError("Message too long to embed.")

    # Embed message in LSB of LH coefficients
    for i in range(len(binary_message)):
        LH_flat[i] = (LH_flat[i] & ~1) | int(binary_message[i])

    # Reshape LH and perform inverse DWT
    LH = LH_flat.reshape(LH.shape)
    stego_image = pywt.idwt2((LL, (LH, HL, HH)), 'haar')
    stego_image = np.clip(stego_image, 0, 255).astype(np.uint8)

    # Save stego image
    cv2.imwrite(output_path, stego_image)
    print(f"Message embedded and saved to {output_path}")


def extract_message(stego_image_path):
    """
    Extracts a message from a stego image using DWT.
    """
    # Read stego image
    stego_image = cv2.imread(stego_image_path, cv2.IMREAD_GRAYSCALE)
    if stego_image is None:
        raise ValueError("Error loading stego image.")

    # Perform DWT
    coeffs2 = pywt.dwt2(stego_image, 'haar')
    LL, (LH, HL, HH) = coeffs2

    # Extract LSBs from LH coefficients
    LH_flat = LH.flatten()
    binary_message = ''.join(str(pixel & 1) for pixel in LH_flat)

    # Convert binary to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        if char == '\0':  # Stop at null terminator
            break
        message += char

    print(f"Extracted Message: {message}")
    return message