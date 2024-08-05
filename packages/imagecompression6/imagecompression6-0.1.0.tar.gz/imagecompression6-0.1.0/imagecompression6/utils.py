import matplotlib.pyplot as plt

def display_images(original, compressed):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(original, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Compressed Image")
    plt.imshow(compressed, cmap='gray')
    plt.axis('off')

    plt.show()
