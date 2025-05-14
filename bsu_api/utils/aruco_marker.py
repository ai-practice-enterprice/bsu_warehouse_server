import os
import cv2
import base64
import numpy as np
from pathlib import Path


def generate_aruco_marker_b64(id: int, size=300) -> str:
    """
    Generates an ArUco marker image with the specified ID and size, and returns it as a Base64-encoded string.

    Args:
        id (int): The ID of the marker (0-1023).
        size (int): The pixel size of the marker.

    Returns:
        base64_str (str): The Base64-encoded string of the marker image.

    Raises:
        ValueError: If the ID is outside the valid range (0-1023).
    """

    if not (0 <= id < 1024):
        raise ValueError("ID must be in the range 0-1023.")

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    marker = cv2.aruco.generateImageMarker(aruco_dict, id, size)
    _, buffer = cv2.imencode(".png", marker)
    base64_str = base64.b64encode(buffer).decode("utf-8")
    return base64_str


def generate_aruco_marker(id: int, size=300, output_dir="") -> str:
    """
    Generates an ArUco marker image with the specified ID and size.

    Args:
        id (int): The ID of the marker (0-1023).
        size (int): The pixel size of the marker.
        output_dir (str): The directory to save the marker image.
  
    Returns:
        filename (str): The filename of the saved marker image.

    Raises:
        FileExistsError: If the file already exists in the output directory.
        ValueError: If the ID is outside the valid range (0-1023).
    """

    if not (0 <= id < 1024):
        raise ValueError("ID must be in the range 0-1023.")

    path = os.path.join(output_dir, f"aruco_marker_{id}.png")
    if os.path.exists(path):
        raise FileExistsError(f"File already exists: {path}")

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    marker = cv2.aruco.generateImageMarker(aruco_dict, id, size)
    cv2.imwrite(path, marker)
    return path


def decode_aruco_id_b64(base64_str: str) -> int:
    """
    Decodes an ArUco marker from a Base64-encoded image and extracts the marker ID.
    
    Args:
        base64_str (str): The Base64-encoded string of the marker image.
        
    Returns:
        marker_id (int): The ID of the detected ArUco marker, or -1 if not found.
    """

    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, dtype=np.uint8) # buffer to np array
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE) # grayscale image

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    _, ids, __ = detector.detectMarkers(img)

    if ids is not None and len(ids) > 0:
        return int(ids[0][0])

    return -1


def decode_aruco_id(image_path: str) -> int:
    """
    Decodes an ArUco marker from an image file and extracts the marker ID.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        marker_id (int): The ID of the detected ArUco marker, or -1 if not found.

    Raises:
        FileNotFoundError: If the image file is not found.
    """

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {image_path}")

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    _, ids, __ = detector.detectMarkers(img)

    if ids is not None and len(ids) > 0:
        return int(ids[0][0])

    return -1
