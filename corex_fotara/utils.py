import base64
import io

import pyqrcode


def qr_to_base64(data, scale=4):
	if not data:
		return ""
	buf = io.BytesIO()
	pyqrcode.create(data, error="M").png(buf, scale=scale)
	return base64.b64encode(buf.getvalue()).decode()
