import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def abs_threshold(img, orient='x', thresh=(20, 100)):
    """
    Apply Sobel x or y, take absolute value and apply threshold.
    Output array of the same size as the input image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply x or y gradient and take absolute value
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
    # Rescale back to 8 bit integer
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))
    # Create a binary mask where scaled gradient magnitude thresholds are met
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh[0]) &
                  (scaled_sobel <= thresh[1])] = 1

    return binary_output


def mag_threshold(img, sobel_kernel=3, mag_thresh=(30, 100)):
    """
    Apply Sobel x or y, compute magnitude value and apply threshold.
    Output array of the same size as the input image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Calculate the magnitude
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    # Scale to 8-bit (0 - 255) and convert to type = np.uint8
    scale_factor = np.max(gradmag) / 255
    gradmag = (gradmag / scale_factor).astype(np.uint8)
    # Create a binary mask where overall magnitude thresholds are met
    binary_output = np.zeros_like(gradmag)
    binary_output[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1

    return binary_output


def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi / 2)):
    """
    Apply Sobel x or y, compute direction of gradient and apply threshold.
    Output array of the same size as the input image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Take the absolute value of the x and y gradients
    # use np.arctan2(abs_sobely, abs_sobelx) to calculate the direction of the
    # gradient
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
    # Create a binary mask where direction thresholds are met
    binary_output = np.zeros_like(absgraddir)
    binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1

    return binary_output


def hls_threshold(img, thresh=(100, 255)):
    """
    Separate S channel from HLS color space and apply threshold
    Output array of the same size as the input image
    """
    # Convert to HLS color space
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    # separate S channel
    s_channel = hls[:, :, 2]
    # Create a binary mask where color thresholds are met
    binary_output = np.zeros_like(s_channel)
    binary_output[(s_channel > thresh[0]) & (s_channel <= thresh[1])] = 1

    return binary_output


def combined_threshold(img):
    """
    Apply combined thresholds using pre-defined functions
    Output array of the same size as the input image
    """
    abs_thresh = abs_threshold(img, orient='x', thresh=(20, 100))
    mag_thresh = mag_threshold(img, sobel_kernel=3, mag_thresh=(30, 100))
    dir_thresh = dir_threshold(img, sobel_kernel=3, thresh=(0.7, 1.3))
    hls_thresh = hls_threshold(img, thresh=(170, 255))

    # Create the final binary mask where combined thresholds are met
    combined_output = np.zeros_like(hls_thresh)
    combined_output[(abs_thresh == 1 | ((mag_thresh == 1) &
                     (dir_thresh == 1))) | hls_thresh == 1] = 1

    return combined_output, abs_thresh, mag_thresh, dir_thresh, hls_thresh


if __name__ == '__main__':
    # Test example image(undistorted)
    image_file = './output_images/undistorted1.jpg'
    image = mpimg.imread(image_file)
    
    # Create binary outputs
    combined_output, abs_thresh, mag_thresh, dir_thresh, hls_thresh = combined_threshold(image)

    # Plot original image and binary output images in order
    plt.subplot(2, 3, 1)
    plt.imshow(image)
    plt.subplot(2, 3, 2)
    plt.imshow(abs_thresh, cmap='gray')
    plt.subplot(2, 3, 3)
    plt.imshow(mag_thresh, cmap='gray')
    plt.subplot(2, 3, 4)
    plt.imshow(dir_thresh, cmap='gray')
    plt.subplot(2, 3, 5)
    plt.imshow(hls_thresh, cmap='gray')
    plt.subplot(2, 3, 6)
    plt.imshow(combined_output, cmap='gray')

    plt.show()