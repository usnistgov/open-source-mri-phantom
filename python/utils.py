import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from math import pi, cos, sin
from scipy import ndimage as ndi
from matplotlib.patches import Wedge

def get_roi_circles(im, threshold, circle_circumference_threshold, min_pixel_x, min_pixel_y, max_pixel_x, max_pixel_y, rmin=6, rmax=7, steps=100):
    """Finds ROIs by searching for circles
        im: 2d numpy array of the image (one slice of interest)
        threshold: Masking threshold fraction for image
        circle_circumference_threshold: The circumference threshold, in other words how much
            of the circumference needs to be "filled in" for the circle to count
        min_pixel_x: Minimum pixel x value for circle center
        min_pixel_y: Minimum pixel y value for circle center
        max_pixel_x: Maximum pixel x value for circle center
        max_pixel_y: Maximum pixel y value for circle center
        rmin: Minimum radius to search for
        rmax: Maximum radius to search for
        steps: Number of steps in the circumference to consider
    """
    # Get the circles and filter out based on limits
    x_mask = im < threshold * np.max(im)
    edges_lo = x_mask.astype(int) - ndi.binary_erosion(x_mask, iterations=3).astype(int)
    circles_lo = get_circles_for_edges(edges_lo, rmin, rmax, steps, circle_circumference_threshold)
    all_circles = [c for c in circles_lo if (c[1] > min_pixel_x) and (c[1] < max_pixel_x) 
                   and (c[0] > min_pixel_y) and (c[0] < max_pixel_y) ] 
    return all_circles


def get_circles_for_edges(edges, rmin, rmax, steps, threshold, debug=False):
    """Finds circles for edges in an image
        steps: Number of steps in the circumference to consider
        threshold: The circumference threshold, in other words how much
            of the circumference needs to be "filled in" for the circle to count
    """
    edge_points = np.argwhere(edges)
    # Points holds all the possible points to be considered on a circle from the edge
    points = []
    for r in range(rmin, rmax + 1):
        for t in range(steps):
            points.append((r, int(r * cos(2 * pi * t / steps)), int(r * sin(2 * pi * t / steps))))

    # Each edge_point can be considered part of a circle. This is a dictionary that has every combination
    acc = defaultdict(int)
    for x, y in edge_points:
        for r, dx, dy in points:
            a = x - dx
            b = y - dy
            acc[(a, b, r)] += 1

    # Circles holds all the valid circles. Valid circles are those for which it isn't already in
    # the circles as a smaller circle, and meets the circle threshold requirement
    circles = []
    for k, v in sorted(acc.items(), key=lambda i: -i[1]):
        x, y, r = k
        if v / steps >= threshold and all((x - xc) ** 2 + (y - yc) ** 2 > rc ** 2 for xc, yc, rc in circles):
            if debug:
                print(v / steps, x, y, r)
            circles.append((x, y, r))
    return circles

def calculate_geom_dist(circles, mm_pixel):
    """Calculate the geometric distances between circles
        circles: List of circles in the format (x, y, r)
        mm_pixel: The number of mm per pixel
    """
    # First sort the circles by x value
    circles = [circles[i] for i in np.argsort([c[0] for c in circles])]
    # Then get distances between circles
    distances = []
    for i in range(len(circles)-1):
        distance = np.sqrt((circles[i+1][0] - circles[i][0])**2 + (circles[i+1][1] - circles[i][1])**2)
        distance = np.round(distance * mm_pixel, decimals=1)
        distances.append(distance)
    return distances

def plot_circles(im, circles):
    """Plot the circles on the image
        im: 2d numpy array of the image (one slice of interest)
        circles: List of circles in the format (x, y, r)
    """
    f, ax = plt.subplots()
    ax.imshow(im, cmap='gray')

    for i in range(len(circles)):
        x, y, r = circles[i]
        w = Wedge((y, x), r, 0, 360, width=1, edgecolor="cyan")
        ax.add_patch(w)
        ax.scatter([c[1] for c in circles], [c[0] for c in circles], color="cyan", marker="x")
    return f, ax

def get_snr_cnr(im, noise_rects, signal_rect):
    """Calculate the SNR and CNR for an image
        im: 2d numpy array of the image (one slice of interest)
        noise_rects: List of rectangles in the format ((x, w), (y, h)) for the noise
        signal_rect: Rectangle in the format ((x, w), (y, h)) for the signal
    """
    
    noise_std = np.std([im[rect[0][0]:rect[0][0] + rect[0][1], rect[1][0]:rect[1][0] + rect[1][1]].flatten()
                         for rect in noise_rects])
    noise_signal = np.mean([im[rect[0][0]:rect[0][0] + rect[0][1], rect[1][0]:rect[1][0] + rect[1][1]].flatten()
                             for rect in noise_rects])
    signal = np.mean(im[signal_rect[0][0]:signal_rect[0][0] + signal_rect[0][1],
                        signal_rect[1][0]:signal_rect[1][0] + signal_rect[1][1]])

    snr = signal/noise_std
    cnr = (signal - noise_signal)/noise_std

    return snr, cnr

def plot_rects(im, noise_rects, signal_rect, ax=None):
    """Plot the rectangles on the image
        im: 2d numpy array of the image (one slice of interest)
        noise_rects: List of rectangles in the format ((x, w), (y, h)) for the noise
        signal_rect: Rectangle in the format ((x, w), (y, h)) for the signal
    """
    if ax is None:
        f, ax = plt.subplots()
    else:
        f = ax.get_figure()
    ax.imshow(im, cmap='gray')

    for rect in noise_rects:
        x, w = rect[0]
        y, h = rect[1]
        ax.add_patch(plt.Rectangle((y, x), h, w, edgecolor="red", facecolor="none"))
    x, w = signal_rect[0]
    y, h = signal_rect[1]
    ax.add_patch(plt.Rectangle((y, x), h, w, edgecolor="green", facecolor="none"))
    return f, ax