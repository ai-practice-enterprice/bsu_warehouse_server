import qrcode
import pathlib
import base64
import io
from PIL import Image
from pyzbar.pyzbar import decode


def decode_qr_code(file_path: str) -> str:
    """
    Read a QR code from a file and return the base64 encoded image
    
    Args:
        file_path (str): The path to the QR code image file

    Returns:
        base64_str (str): The base64 encoded image

    Raises:
        FileNotFoundError: If the file does not exist
    """
    path = pathlib.Path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File {file_path} not found")
    
    img = Image.open(file_path)
    decoded_text = decode(img)[0].data.decode("utf-8")
    return decoded_text


def decode_qr_code_b64(base64_str: str) -> str:
    """
    Decode a base64 encoded QR code image and return the decoded text
    
    Args:
        base64_str (str): The base64 encoded image

    Returns:
        decoded_text (str): The decoded text from the QR code
    """
    
    img_bytes = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_bytes))
    decoded_text = decode(img)[0].data.decode("utf-8")
    return decoded_text


def generate_qr_code(data: str, file_path: str) -> str:
    """
    Generate a QR code image from the given data and save it to a file
    
    Args:
        data (str): The text or data to encode in the QR code
        file_path (str): The path to save the QR code image file

    Returns:
        file_path (str): The path to the saved QR code image file

    Raises:
        FileExistsError: If the file already exists
    """
    path = pathlib.Path(file_path)
    if path.exists():
        raise FileExistsError(f"File {file_path} already exists")

    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path) # type:ignore
    return file_path


def generate_qr_code_b64(data: str) -> str:
    """
    Encode a QR code image from the given data and return the base64 encoded image
    
    Args:
        data (str): The text or data to encode in the QR code

    Returns:
        base64_str (str): The base64 encoded image
    """
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG") # type:ignore
    img_bytes.seek(0)
    
    base64_str = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    return base64_str
