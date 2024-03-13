from PIL import Image, ImageOps
def add_white_borders_to_fit_4_5_aspect_ratio(image_path, output_path):
    # Load the image
    image = Image.open(image_path)

    # Target aspect ratio
    target_ratio = (4, 5)

    # Original image size and aspect ratioj
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

    # Save the modified image
    new_image.save(output_path)

    print(f"Modified image saved to: {output_path}")

# Replace these paths with the appropriate paths on your system
image_path = '/Users/chinmaybansal/Photogrpahy/Turkey Run/DSC_0427.JPG'
output_path = '/Users/chinmaybansal/Downloads/DSC_0427_instagram_ready.JPG'

# Run the function
add_white_borders_to_fit_4_5_aspect_ratio(image_path, output_path)
