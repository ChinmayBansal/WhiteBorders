from PIL import Image, ImageOps,  ExifTags
from io import BytesIO

def add_white_borders_to_fit_4_5_aspect_ratio(input_image_stream, output_buffer):
    # Load the image from the file stream
    image = Image.open(input_image_stream)

    # Correct orientation based on EXIF data
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Cases: image doesn't have getexif
        pass


    # Target aspect ratio
    target_ratio = (4, 5)

    # Original image size and aspect ratio
    original_width, original_height = image.size
    original_ratio = original_width / original_height

    # Calculate new size based on the target 4:5 ratio
    if original_ratio > (target_ratio[0] / target_ratio[1]):
        # Wider than 4:5, adjust height
        new_height = int(original_width / (target_ratio[0] / target_ratio[1]))
        new_size = (original_width, new_height)
    else:
        # Taller than 4:5, adjust width
        new_width = int(original_height * (target_ratio[0] / target_ratio[1]))
        new_size = (new_width, original_height)

    # Add white borders to the original image to fit the new size
    new_image = ImageOps.expand(image, border=(
        0, max(0, (new_size[1] - original_height) // 2), 0, max(0, (new_size[1] - original_height) // 2)), fill='white')
    new_image = ImageOps.expand(new_image, border=(
        max(0, (new_size[0] - original_width) // 2), 0, max(0, (new_size[0] - original_width) // 2), 0), fill='white')

    # Save the modified image to the output buffer
    new_image.save(output_buffer, format='JPEG')  # Adjust the format if necessary

    # Important: You must rewind the buffer to the beginning so it's ready for reading.
    output_buffer.seek(0)
