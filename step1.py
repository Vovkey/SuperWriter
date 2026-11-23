import cv2
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt

img = cv2.imread("test.jpeg")
if img is None:
    raise FileNotFoundError("Couldn't load the image -check the path")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
print("Image size (height, width):", gray.shape)

blur = cv2.GaussianBlur(gray, (5, 5), 0)

_, otsu = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

adaptive = cv2.adaptiveThreshold(
    blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31, 10,
)

titles = ["Grayscale", "Otsu", "Adaptive"]
images = [gray, otsu, adaptive]
for i, (t, im) in enumerate(zip(titles, images), start=1):
    plt.subplot(1, 3, i)
    plt.imshow(im, cmap="gray")
    plt.title(t)
    plt.axis("off")
plt.show()
