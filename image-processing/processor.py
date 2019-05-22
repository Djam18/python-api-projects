from PIL import Image
import io


def resize_image(image_bytes, width, height):
    img = Image.open(io.BytesIO(image_bytes))
    resized = img.resize((width, height))
    output = io.BytesIO()
    resized.save(output, format=img.format or 'PNG')
    return output.getvalue()


def crop_image(image_bytes, x, y, width, height):
    img = Image.open(io.BytesIO(image_bytes))
    cropped = img.crop((x, y, x + width, y + height))
    output = io.BytesIO()
    cropped.save(output, format=img.format or 'PNG')
    return output.getvalue()


def rotate_image(image_bytes, degrees):
    img = Image.open(io.BytesIO(image_bytes))
    rotated = img.rotate(degrees, expand=True)
    output = io.BytesIO()
    rotated.save(output, format=img.format or 'PNG')
    return output.getvalue()


def grayscale_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    gray = img.convert('L')
    output = io.BytesIO()
    gray.save(output, format=img.format or 'PNG')
    return output.getvalue()


def flip_image(image_bytes, direction='horizontal'):
    img = Image.open(io.BytesIO(image_bytes))
    if direction == 'horizontal':
        flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
    output = io.BytesIO()
    flipped.save(output, format=img.format or 'PNG')
    return output.getvalue()
