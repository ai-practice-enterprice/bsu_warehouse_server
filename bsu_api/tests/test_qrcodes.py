from utils.qrcodes import generate_qr_code_b64, decode_qr_code_b64


def test_qr_code():
    url = "https://www.google.com"
    qr_code_b64 = generate_qr_code_b64(url)
    assert decode_qr_code_b64(qr_code_b64) == url 
