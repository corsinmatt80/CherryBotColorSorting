from backend.camera.camera_stream import save_image
import cv2
import numpy as np

def detect_baskets():

    save_image('frontend/static/baskets')
    baskets_image = cv2.imread('frontend/static/baskets.jpg')

    #there exists a library to do this with pre given functions
    #we did it manually on purpose to understand the whole process

    gray_baskets = convert_gray(baskets_image)
    blurred_baskets = gaussian_blurr(gray_baskets,5,1.5)

    edges = sobel_edge_detection(blurred_baskets)
    edge_image = color_edges(baskets_image, edges)

    # Display the image with contours
    cv2.imshow('Edges', edge_image)
    cv2.imshow("Baskets", baskets_image)



    #image_round_figures, rounds = detect_round_figures(baskets_image.copy(),edges,5,5)
    #cv2.imshow('Rounds', image_round_figures)



    image_square_figures, squares = detect_square_figures(baskets_image.copy(),edges)
    cv2.imshow('Squares', image_square_figures)
    
    image_path = 'static/baskets.jpg'

    # Return the path for use in the frontend
    return image_path, squares


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
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]
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

def color_edges(image, edges, edge_color  = (255,0,0), threshold = 35):
    edges_mask = edges > threshold
    #copy the original image to modify
    edges_colored = image.copy()

    for c in range(3):  #iterate through channels and modify pixel
        edges_colored[:, :, c][edges_mask] = edge_color[c]

    return edges_colored


def detect_round_figures(image, edges, rad, circ):
    #function for finding contours
    #those are objects or figures that are closed
    edge_mask = (edges > 75).astype(np.uint8)
    contours,_ = cv2.findContours(edge_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    round_figures = []

    for contour in contours:
        #this function draws the minimum possible circle around the contour
        ((x,y), radius) = cv2.minEnclosingCircle(contour)
        #formula for how close the figure is to a circle
        #cv2.contourArea : area of contour
        #cv2.arcLength : circumference
        circularity = (4 * np.pi * cv2.contourArea(contour)) / (cv2.arcLength(contour, True) * 2 + 1e-5)
        if radius > rad and circularity > circ:
            round_figures.append((contour, (int(x), int(y), int(radius))))
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            cv2.circle(image, (int(x), int(y)), int(radius), (255, 0, 0), 2)
            cv2.circle(image, (int(x), int(y)), 3, (0, 0, 255), -1)

    return image, round_figures

def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype(np.float32), (p2 - p1).astype(np.float32)
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))

def is_overlapping(rect1, rect2, threshold=0.1):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    overlap_area = overlap_x * overlap_y

    area1 = w1 * h1
    area2 = w2 * h2

    return overlap_area / min(area1, area2) > threshold
    
def detect_square_figures(image, edges):
    #function for finding contours
    #those are objects or figures that are closed
    edge_mask = (edges > 35).astype(np.uint8)
    contours, _ = cv2.findContours(edge_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    square_figures = []

    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        #approxPolyDP : stores edges
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4 and cv2.contourArea(contour) > 100:
            # Check if the contour is in the shape of a square
            approx = approx.reshape(-1, 2)
            max_cos = np.max([angle_cos(approx[i], approx[(i+1) % 4], approx[(i+2) % 4]) for i in range(4)])
            if max_cos < 0.2:  # Threshold for cosine of 90 degrees
                if not any(is_overlapping(cv2.boundingRect(approx), cv2.boundingRect(existing)) for existing in square_figures):
                    square_figures.append(approx)
            

    return image, square_figures
