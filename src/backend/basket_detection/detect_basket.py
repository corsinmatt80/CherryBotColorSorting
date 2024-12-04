from backend.camera.camera_stream import save_image
import cv2
import numpy as np

def detect_baskets():
    save_image('baskets')
    baskets_image = cv2.imread('../assets/baskets.jpg')

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
    # Save processed images for display
    processed_image_path = "../frontend/static/processed_baskets.jpg"
    cv2.imwrite(processed_image_path, image_square_figures)

    # Return the path for use in the frontend
    return processed_image_path, squares


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
            #boundingRect : finds a rectangle around for the four points
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 0.8 <= aspect_ratio <= 1.2:
                square_figures.append(approx)
                cv2.drawContours(image, [approx], -1, (0,255,0),2)

    return image, square_figures

detect_baskets()