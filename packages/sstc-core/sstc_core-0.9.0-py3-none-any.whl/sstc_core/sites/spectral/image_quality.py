import cv2
import numpy as np
from PIL import Image as PILImage
from sstc_core.sites.spectral.io_tools import load_yaml


def convert_to_bool(value):
    """
    Converts a value to a boolean type. This function handles different types of boolean-like values
    and ensures that the output is a standard Python boolean (`True` or `False`).

    Parameters:
        value (Any): The input value to be converted to a boolean. This can include various types
                     such as numpy boolean types, Python boolean types, or other values.

    Returns:
        bool: The converted boolean value. If the input value is a boolean type (numpy or Python),
              it returns the corresponding boolean value. For any other input, it returns `False`.

    Examples:
        ```python
        >>> convert_to_bool(np.bool_(True))
        True

        >>> convert_to_bool(True)
        True

        >>> convert_to_bool(False)
        False

        >>> convert_to_bool(1)
        False

        >>> convert_to_bool("string")
        False
        ```
    """
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    return False


def detect_blur(image, method='laplacian', threshold=100):
    """
    Detect if an image is blurry using specified metrics.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        method (str): The method used for blurriness detection. Options are 'laplacian' and 'sobel'.
        threshold (float): The threshold value for blurriness detection. If the computed metric is below this threshold, the image is considered blurry.

    Returns:
        bool: True if the image is detected as blurry, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)

        # Detect blur using Laplacian method
        is_blurry = detect_blur(image, method='laplacian', threshold=100)
        print(f"Laplacian method - Is image blurry? {is_blurry}")

        # Detect blur using Sobel method
        is_blurry_sobel = detect_blur(image, method='sobel', threshold=10)
        print(f"Sobel method - Is image blurry? {is_blurry_sobel}")        
        
        ```
    """
    if not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a numpy ndarray.")
    if method not in ['laplacian', 'sobel']:
        raise ValueError("Invalid method. Choose 'laplacian' or 'sobel'.")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if method == 'laplacian':
        # Compute the Laplacian variance as the measure of blurriness
        blur_value = cv2.Laplacian(gray, cv2.CV_64F).var()
    elif method == 'sobel':
        # Compute the Sobel gradient magnitude as the measure of blurriness
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_mag = np.sqrt(sobelx**2 + sobely**2)
        blur_value = np.mean(sobel_mag)
    
    # Determine if the image is blurry based on the threshold
    return convert_to_bool(blur_value < threshold)


def detect_snow(image, brightness_threshold=200, saturation_threshold=50):
    """
    Detect snow in an image based on brightness and saturation thresholds.
    
    Snowflakes often appear as bright white spots with varying sizes. A simple approach 
    is to identify regions in the image with high brightness and low saturation.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        brightness_threshold (int): The minimum brightness value to consider as snow.
        saturation_threshold (int): The maximum saturation value to consider as snow.

    Returns:
        bool: True if snow is detected, False otherwise.
        
    Example:
        ```python
            image_path = 'image.jpg'
            image = cv2.imread(image_path)
            if detect_snow(image):
                print("Snow detected")
            else:
                print("No snow detected")
        ```
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = hsv[:, :, 2]
    saturation = hsv[:, :, 1]

    snow_mask = (brightness > brightness_threshold) & (saturation < saturation_threshold)
    snow_percentage = np.sum(snow_mask) / (image.shape[0] * image.shape[1])

    return convert_to_bool(snow_percentage > 0.01)  # Adjust percentage threshold as needed


def detect_rain(image, min_line_length=100, max_line_gap=10):
    """
    Detect rain in an image using line detection.
    
    Rain can be detected by analyzing the vertical streaks or lines in an image. This can be achieved
    using edge detection and line detection techniques.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_line_length (int): Minimum line length to be considered as rain.
        max_line_gap (int): Maximum gap between line segments to be considered as a single line.

    Returns:
        bool: True if rain is detected, False otherwise.
        
    Example:
        ```python
            image_path = 'image.jpg'
            image = cv2.imread(image_path)
            if detect_rain(image):
                print("Rain detected")
            else:
                print("No rain detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=min_line_length, maxLineGap=max_line_gap)
    
    if lines is not None:
        return True
    return False


def detect_water_drops(image, min_radius=5, max_radius=20):
    """
    Detect water drops on the lens using circular Hough Transform.
    
    Water drops on the lens create localized distortions. 
    Detecting them involves looking for circular regions with different 
    textures or colors.
    

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_radius (int): Minimum radius of water drops to detect.
        max_radius (int): Maximum radius of water drops to detect.

    Returns:
        bool: True if water drops are detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_water_drops(image):
            print("Water drops detected")
        else:
            print("No water drops detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=100, param2=30, minRadius=min_radius, maxRadius=max_radius)
    
    if circles is not None:
        return True
    return False

def detect_dirt(image, min_area=500, max_area=2000):
    """
    Detect dirt on the lens using blob detection.
    
    Dirt on the lens often creates localized dark spots or blobs. 
    This can be detected using blob detection techniques.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_area (int): Minimum area of the dirt blobs to detect.
        max_area (int): Maximum area of the dirt blobs to detect.

    Returns:
        bool: True if dirt is detected, False otherwise.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    
    for stat in stats[1:]:  # Skip the first component as it's the background
        area = stat[cv2.CC_STAT_AREA]
        if min_area < area < max_area:
            return True
    return False


def detect_obstructions(image, min_contour_area=10000):
    """
    Detect obstructions in the image using contour detection to find large objects.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_contour_area (int): Minimum contour area to be considered as an obstruction.

    Returns:
        bool: True if obstructions are detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_obstructions(image):
            print("Obstruction detected")
        else:
            print("No obstruction detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_contour_area:
            return True
    return False


def assess_brightness(image, dark_threshold=50, bright_threshold=200):
    """
    Assess the brightness of an image and return a status code.
    
    Assessing brightness involves calculating the average intensity of the image and checking it 
    against thresholds for too dark or too bright conditions.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        dark_threshold (int): The brightness value below which the image is considered too dark.
        bright_threshold (int): The brightness value above which the image is considered too bright.

    Returns:
        int: 0 if brightness is optimal, -1 if very dark, 1 if very bright.
    
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        brightness_status = assess_brightness(image)
        
        if brightness_status == -1:
            print("Very dark image")
        elif brightness_status == 1:
            print("Very bright image")
        else:
            print("Optimal brightness")        
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    average_brightness = np.mean(gray)

    if average_brightness < dark_threshold:
        return 1  # Very dark image
    elif average_brightness > bright_threshold:
        return 1  # Very bright image
    else:
        return 0  # Optimal brightness
    
    
def detect_glare(image, threshold=240):
    """
    Detect glare in an image based on pixel value thresholds.
    
    Detecting glare involves identifying overexposed areas in the image, 
    usually found in bright regions.


    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        threshold (int): The pixel value threshold above which pixels are considered to have glare.

    Returns:
        bool: True if glare is detected, False otherwise.
    
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_glare(image):
            print("Glare detected")
        else:
            print("No glare detected")        
        ```
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    _, _, v = cv2.split(hsv)
    glare_mask = v > threshold
    glare_percentage = np.sum(glare_mask) / (image.shape[0] * image.shape[1])

    return convert_to_bool(glare_percentage > 0.01)  # Adjust percentage threshold as needed


def detect_fog(image, threshold=0.5):
    """
    Detect fog in an image by analyzing edge detection.
    
    Detecting fog involves analyzing the contrast in the image, as fog often reduces contrast.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        threshold (float): The ratio of edge pixels to total pixels below which the image is considered foggy.

    Returns:
        bool: True if fog is detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_fog(image):
            print("Fog detected")
        else:
            print("No fog detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = np.sum(edges > 0) / (image.shape[0] * image.shape[1])

    return convert_to_bool(edge_ratio < threshold)


def detect_rotation(image, angle_threshold=10):
    """
    Detect if an image has been rotated by analyzing the orientation of lines.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        angle_threshold (float): The angle threshold above which the image is considered rotated.

    Returns:
        bool: True if significant rotation is detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_rotation(image):
            print("Image rotation detected")
        else:
            print("No significant image rotation detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta)
            angle = (angle - 90) % 180  # Normalize angle
            angles.append(angle)

        average_angle = np.mean(angles)
        return convert_to_bool(abs(average_angle) > angle_threshold)

    return False


def assess_image_quality(image, flag_other:0, flag_birds:0):
    """
    Assess the quality of an image by evaluating brightness, glare, fog,  and rotation.
    Handles image inputs as PIL image, OpenCV image, or file path.

    Parameters:
        image (Union[str, PILImage.Image, np.ndarray]): The input image as a file path, PIL image, or OpenCV image.

    Returns:
        dict: A dictionary containing the results of the quality assessment.
    """
    # Determine the type of input and process accordingly
    if isinstance(image, str):
        # If input is a file path, load the image using OpenCV
        image = cv2.imread(image)
        if image is None:
            raise ValueError(f"Image file at {image} could not be loaded.")
    elif isinstance(image, PILImage.Image):
        # If input is a PIL image, convert it to OpenCV format
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif isinstance(image, np.ndarray):
        # If input is already an OpenCV image, ensure it's in BGR format
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = image
        else:
            raise ValueError("OpenCV image must be a 3-channel BGR image.")
    else:
        raise TypeError("Input must be a file path, PIL image, or OpenCV image.")

    # Perform various quality assessments
    # Store the results in a dictionary with expected names for the quality index function
    quality_assessment_results = {
        'flag_brightness': assess_brightness(image),
        'flag_blur': detect_blur(image),  # Add blur detection
        'flag_snow': detect_snow(image),  # Add snow detection
        'flag_rain': detect_rain(image),  # Add rain detection
        'flag_water_drops': detect_water_drops(image),  # Add water drops detection
        'flag_dirt': detect_dirt(image),  # Add dirt detection
        'flag_obstructions': detect_obstructions(image),  # Add obstructions detection
        'flag_glare': detect_glare(image),
        'flag_fog': detect_fog(image),
        'flag_rotation': detect_rotation(image),
        'flag_birds': flag_birds,        
        'flag_other': flag_other,        
    }

    return quality_assessment_results


def load_weights_from_yaml(yaml_file=str, station_name='default', platform_id='default'):
    """
    Load weights from a YAML file for a specific station and platform.

    Parameters:
        yaml_file (str): Path to the YAML file.
        station_name (str): Station name to select the weights set (default is 'default').
        platform_id (str): Platform ID to select the weights set (default is 'default').

    Returns:
        dict: Dictionary containing weights for each quality factor.
    """
    
    weights = load_yaml(yaml_file)

    # Load weights based on station and platform, fallback to default if not found
    station_weights = weights.get(station_name, weights['default'])
    return station_weights.get(platform_id, station_weights)


def calculate_normalized_quality_index(quality_flags_dict:dict, weights:dict):
    """
    Calculate a composite quality index based on various image assessments with weights from a YAML file.

    Parameters:
        weights (dict): Dictionary containing weights for each quality factor.
        quality_flags_dict (dict): Dictionary containing results from the image quality assessment.

    Returns:
        tuple:
            float: The normalized quality index (0 to 1 scale).
            str: weights version used.
        
    Example:
        ```python
        # Load weights from the YAML file for a specific station and platform
        station_name = 'Abisko'
        platform_id = 'platform_1'
        weights = load_weights_from_yaml('weights.yaml', station_name, platform_id)

        # Example quality assessment results
        quality_assessment_results = {
            'flag_brightness': 0,  # Example value
            'flag_blur': True,
            'flag_snow': True,
            'flag_rain': False,
            'flag_water_drops': False,
            'flag_dirt': False,
            'flag_obstructions': False,
            'flag_glare': False,
            'flag_fog': False,
            'flag_rotation': False,
            'flag_birds': False,
            'flag_other': False,
        }

        # Calculate the normalized quality index
        quality_index = calculate_quality_index(weights, quality_assessment_results)
        print(f"Normalized Quality Index: {quality_index:.2f}")
        ```
    """
    # Extract results from the quality assessment dictionary
    flag_brightness = quality_flags_dict.get('flag_brightness', False)
    flag_blur = quality_flags_dict.get('flag_blur', False)
    flag_snow = quality_flags_dict.get('flag_snow', False)
    flag_rain = quality_flags_dict.get('flag_rain', False)
    flag_water_drops = quality_flags_dict.get('flag_water_drops', False)
    flag_dirt = quality_flags_dict.get('flag_dirt', False)
    flag_obstructions = quality_flags_dict.get('flag_obstructions', False)
    flag_glare = quality_flags_dict.get('flag_glare', False)
    flag_fog = quality_flags_dict.get('flag_fog', False)
    flag_rotation = quality_flags_dict.get('flag_rotation', False)
    flag_birds = quality_flags_dict.get('flag_birds', False)
    flag_other = quality_flags_dict.get('flag_other', False)

    # Extract weights from the dictionary
    weight_brightness = weights.get('flag_brightness_weight', 0)
    weight_blur = weights.get('flag_blur_weight', 0)
    weight_snow = weights.get('flag_snow_weight', 0)
    weight_rain = weights.get('flag_rain_weight', 0)
    weight_water_drops = weights.get('flag_water_drops_weight', 0)
    weight_dirt = weights.get('flag_dirt_weight', 0)
    weight_obstructions = weights.get('flag_obstructions_weight', 0)
    weight_glare = weights.get('flag_glare_weight', 0)
    weight_fog = weights.get('flag_fog_weight', 0)
    weight_rotation = weights.get('flag_rotation_weight', 0)
    weight_birds = weights.get('flag_birds_weight', 0)
    weight_other = weights.get('flag_other_weight', 0)
    quality_index_weights_version = weights.get('quality_index_weights_version', "0.1")
    

    # Convert boolean flags to numeric scores
    brightness_score = 1 if not flag_brightness else 0
    blur_score = 1 if not flag_blur else 0
    snow_score = 1 if not flag_snow else 0  # Moderate impact if snow is detected
    rain_score = 1 if not flag_rain else 0
    water_drops_score = 1 if not flag_water_drops else 0
    dirt_score = 1 if not flag_dirt else 0
    obstructions_score = 1 if not flag_obstructions else 0
    glare_score = 1 if not flag_glare else 0
    fog_score = 1 if not flag_fog else 0
    rotation_score = 1 if not flag_rotation else 0
    birds_score = 1 if not flag_birds else 0
    other_score = 1 if not flag_other else 0

    # Combine the scores with weights
    raw_quality_index = (weight_brightness * brightness_score +
                         weight_blur * blur_score +
                         weight_snow * snow_score +
                         weight_rain * rain_score +
                         weight_water_drops * water_drops_score +
                         weight_dirt * dirt_score +
                         weight_obstructions * obstructions_score +
                         weight_glare * glare_score +
                         weight_fog * fog_score +
                         weight_rotation * rotation_score +
                         weight_birds * birds_score +
                         weight_other * other_score)

    # Normalize the quality index to be between 0 and 1
    # Assuming that the maximum possible value is the sum of all weights.
    max_possible_value = (weight_brightness + weight_blur + weight_snow +
                          weight_rain + weight_water_drops + weight_dirt +
                          weight_obstructions + weight_glare + weight_fog +
                          weight_rotation + weight_birds + weight_other)
    
    normalized_quality_index = raw_quality_index / max_possible_value

    return normalized_quality_index, quality_index_weights_version