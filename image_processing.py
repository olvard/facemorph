
from PIL import Image
import io
import base64

def crop_image(image_data, crop_size=(50, 50)):
    """Crop the uploaded image to a specific size (10x10 in this case)."""
    # Load image from the byte stream
    image = Image.open(io.BytesIO(image_data))
    
    # Resize or crop the image to fit the desired size
    cropped_image = image.resize(crop_size, Image.LANCZOS)
    
    # Save cropped image to a byte stream
    output = io.BytesIO()
    cropped_image.save(output, format='PNG')
    output.seek(0)
    
    # Base64 encode the image
    encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')
    
    # Return the base64-encoded content of the cropped image
    return encoded_image