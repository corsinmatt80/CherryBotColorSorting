from src.camera.camera_stream import save_image
import cv2
import numpy as np

def detect_baskets():
    save_image('baskets.jpg')
    baskets_image = cv2.imread('../assets/baskets.jpg')

    #there exists a library to do this with pre given functions
    #we did it manually on purpose to understand the whole process

    gray_baskets = convert_gray(baskets_image)
    blurred_baskets = gaussian_blurr(gray_baskets,5,1.5)

    edges = sobel_edge_detection(blurred_baskets)
    edge_image = color_edges(baskets_image, edges)

    # Display the image with contours
    cv2.imshow('Contours', edge_image)
    cv2.waitKey(10000)


def convert_gray(image):
    """
    gray scale conversion formula : 0.299 * Red + 0.587 * Green + 0.114 * Blue
    image with 3 colors has the following format: (W, H, 3) where 3 is the amount of layers
    each layer represents one color
    """
    blue, green, red = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    #apply formula
    gray_image = (0.299 * red + 0.587 * green + 0.114 * blue)
    return gray_image

def gaussian_blurr(image, kernel_size, sigma):
    kernel = cv2.getGaussianKernel(kernel_size, sigma)
    gaussian_kernel = np.outer(kernel, kernel)

    blurred_image = cv2.filter2D(image, -1, gaussian_kernel)
    return blurred_image

def sobel_edge_detection(image):
    #initialize both sobel matrices
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    sobel_y = np.array([
        [
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]
        ]
    ])
    #get dimensions of the image
    rows,cols = image.shape
    #initialize gradient matrices with the same size as the image and fill it with zeros
    gradient_x = np.zeros_like(image, dtype=np.float32)
    gradient_y = np.zeros_like(image, dtype=np.float32)

    #do the convolution and ignore border pixels
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            #get a 3x3 region of the image
            region = image[i-1:i+2, j-1:j+2]
            #calculate gradients
            gx = np.sum(sobel_x * region)
            gy = np.sum(sobel_y * region)
            #store gradients in respective matrice
            gradient_x[i, j] = gx
            gradient_y[i, j] = gy

    #calculate the magnitude, which is the rate of change of pixel intensity
    #so the higher the magnitude the more likely the pixel is on an edge
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    #normalize magnitude (because pixel range is between 0 and 255
    magnitude = (magnitude / magnitude.max()) * 255
    #convert it for compatibility reasons
    return magnitude.astype(np.uint8)

def color_edges(image, edges, edge_color  = (255,0,0), threshold = 40):
    edges_mask = edges > threshold
    #copy the original image to modify
    edges_colored = image.copy()

    for c in range(3):  #iterate through channels and modify pixel
        edges_colored[:, :, c][edges_mask] = edge_color[c]

    return edges_colored


def detect_round_figures():
    pass

def detect_square_figures():
    pass

detect_baskets()