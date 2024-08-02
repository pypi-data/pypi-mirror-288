from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import argparse
import os
import sys

# Load image
def load_image(image_path):
    return Image.open(image_path)

# Save new image
def save_image(image, output_path, quality = 100):
    image.save(output_path, quality = quality)

# ===== IMAGE PROCESSING =====
# Crop image
def crop_image(image, left, top, right, bottom):
    return image.crop((left, top, right, bottom))

# Adjust exposure
def adjust_ev(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# Adjust saturation
def adjust_sat(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

# Adjust contrast
def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# Adjust sharpness
def adjust_sharpness(image, factor):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

# Blur image: box blur
def box_blur(image, radius):
    blurred_image = image.filter(ImageFilter.BoxBlur(radius))
    return blurred_image

# Blur image: Gaussian blue
def gaussian_blur(image, radius):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
    return blurred_image

# Edge detection
def edge_detect(image):
    return image.filter(ImageFilter.FIND_EDGES)

# Noise reduction
def reduce_noise(image, factor):
    return image.filter(ImageFilter.MedianFilter(size = factor))

# Convert to BW
def bw(image):
    black_and_white = image.convert("L")
    return black_and_white

# Invert colors
def invert(image):
    inverted = ImageOps.invert(image)
    return inverted

# Make thumbnails
def create_thumbnail(image, size):
    thumbnail = image.copy()
    thumbnail.thumbnail(size)
    return thumbnail

# Get image size
def get_image_size(image):
    return image.size

# Get image metadata
def get_metadata(image):
    metadata = image._getexif()
    if metadata is not None:
        exif_data = {}
        relevant_tags = {
            271: "Make",
            272: "Model",
            305: "Software",
            306: "DateTime",
            33432: "Copyright",
            315: "Artist",
            37386: "FocalLength",
            33434: "ExposureTime",
            33437: "FNumber",
            34855: "ISOSpeedRatings",
            42036: "LensModel"
        }

        for tag, value in metadata.items():
            if tag in relevant_tags:
                tag_name = relevant_tags[tag]
                exif_data[tag_name] = value
        
        return exif_data
    else:
        return {}

# Rotate image 90 degrees
def rotate_90(image):
    rotated_image = image.transpose(Image.ROTATE_90)
    return rotated_image

# Rotate image 180 degrees
def rotate_180(image):
    rotated_image = image.transpose(Image.ROTATE_180)
    return rotated_image

# Rotate image 180 degrees
def rotate_270(image):
    rotated_image = image.transpose(Image.ROTATE_270)
    return rotated_image

# Flip image horizontally
def flip_horiz(image):
    flip_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return flip_image

# Flip image vertically
def flip_vert(image):
    flip_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return flip_image

# ===== IMAGE CONVERSION =====
def convert_image(image, output_format):
    output_image = image.convert("RGB") if output_format in ['jpg', 'jpeg'] else image
    return output_image

def display_intro_message():
    intro_message = """
 ____  __  _  _  __       ___  __    __  
(  _ \(  )( \/ )(  )___  / __)(  )  (  ) 
 ) __/ )(  )  (  )((___)( (__ / (_/\ )(  
(__)  (__)(_/\_)(__)     \___)\____/(__) 

pixi - Command-line image processing tool

Usage:    pixi <image_path> [options]
    pixi <image_path> --output_path <output_path> --exposure EV --contrast LEVEL
    pixi <image_path> --size
    pixi <image_path> --convert png

pixi is a tool for performing various image processing tasks such as
adjusting exposure, contrast, saturation, converting image formats, and more.

Example:

    $ pixi image.jpg --output_path processed_image.jpg --exposure 1.5 --contrast 1.2

For a full list of options, use pixi --h or pixi --help.
"""
    print(intro_message)


def main():
    parser = argparse.ArgumentParser(description="pixi-cli")

    parser.add_argument("image_path",help="Path to the input image")

    parser.add_argument("--output_path", help="Path to save the processed image (optional if only checking size or fetching metadata)")

    parser.add_argument("--crop", nargs=4, type=int, metavar=('LEFT', 'TOP', 'RIGHT', 'BOTTOM'), help="Crop image to the specified box")

    parser.add_argument("--exposure", type=float, metavar='EV',
                    help="Adjust exposure by a certain number of exposure values (e.g., +1.0, -0.5)")

    parser.add_argument("--saturation", type=float, metavar='LEVEL', 
                    help="Adjust saturation level (e.g., 1.0 for no change, 0.0 to desaturate, 2.0 to increase saturation)")

    parser.add_argument("--contrast", type=float, metavar='LEVEL', 
                    help="Adjust contrast level (e.g., 1.0 for no change, 0.5 to decrease contrast, 1.5 to increase contrast)")

    parser.add_argument("--sharpness", type=float, metavar='LEVEL', 
                    help="Adjust sharpness level (e.g., 1.0 for no change, 0.5 for softer, 2.0 for sharper)")

    parser.add_argument("--box_blur", type=float, metavar='RADIUS', 
                    help="Apply box blur with the specified radius (e.g., 1.0 for minimal blur, higher values for more blur)")

    parser.add_argument("--gaussian_blur", type=float, metavar='RADIUS', 
                    help="Apply Gaussian blur with the specified radius (e.g., 1.0 for minimal blur, higher values for more blur)")

    parser.add_argument("--reduce_noise", action='store_true', help = "Reduce image noise")

    parser.add_argument("--edge_detect", action='store_true', help = "Detect edges in image")

    parser.add_argument("--bw", action='store_true', help = "Convert to black and white")

    parser.add_argument("--invert", action='store_true', help = "Invert colors")

    parser.add_argument("--size", action='store_true', help="Get image size")

    parser.add_argument("--thumbnail", nargs=2, type=int, metavar=('width', 'height'), help="Create thumbnail")

    parser.add_argument("--compression", type=int, metavar='AMOUNT', help="Compress image to specified quality (1-100)")

    parser.add_argument("--metadata", action='store_true', help="Get image metadata")

    parser.add_argument("--rotate90", action='store_true', help="Rotate image 90 degrees")

    parser.add_argument("--rotate180", action='store_true', help="Rotate image 180 degrees")

    parser.add_argument("--rotate270", action='store_true', help="Rotate image 270 degrees")

    parser.add_argument("--flip_horiz", action='store_true', help="Flip image horizontally")

    parser.add_argument("--flip_vert", action='store_true', help="Flip image vertically")

    parser.add_argument("--convert", metavar='FORMAT', help="Convert image to specified format (e.g., 'png', 'jpg', 'bmp', 'gif', 'tiff', 'svg')")

    # Check if any arguments are passed
    if len(sys.argv) == 1:
        display_intro_message()
        sys.exit()

    args = parser.parse_args()

    image = load_image(args.image_path)

    if args.size:
        width, height = get_image_size(image)
        print(f"Image size: {width}x{height}")

    if args.metadata:
        metadata = get_metadata(image)
        for key, value in metadata.items():
            print(f"{key}: {value}")

    if args.crop or args.exposure or args.saturation or args.contrast or args.sharpness or args.box_blur or args.gaussian_blur or args.reduce_noise or args.edge_detect or args.bw or args.invert or args.thumbnail or args.compression is not None:
        if not args.output_path:
            parser.error("--output_path is required when performing image processing operations")
        
        if args.crop:
            image = crop_image(image, *args.crop)
        if args.exposure:
            image = adjust_ev(image, args.exposure)
        if args.saturation:
            image = adjust_sat(image, args.saturation)
        if args.contrast:
            image = adjust_contrast(image, args.contrast)
        if args.sharpness:
            image = adjust_sharpness(image, args.sharpness)
        if args.box_blur:
            image = box_blur(image, args.box_blur)
        if args.gaussian_blur:
            image = gaussian_blur(image, args.gaussian_blur)
        if args.reduce_noise:
            image = reduce_noise(image, args.reduce_noise)
        if args.edge_detect:
            image = edge_detect(image)
        if args.thumbnail:
            image = create_thumbnail(image, tuple(args.thumbnail))
        if args.bw:
            image = bw(image)
        if args.invert:
            image = invert(image)

        quality = args.compression if args.compression else 100
        save_image(image, args.output_path, quality = quality)

    if args.rotate90 or args.rotate180 or args.rotate270 or args.flip_horiz or args.flip_vert:
        if args.output_path:
            output_path = args.output_path
        else:
            output_path = args.image_path
        if args.rotate90:
            image = rotate_90(image)
        if args.rotate180:
            image = rotate_180(image)
        if args.rotate270:
            image = rotate_270(image)
        if args.flip_horiz:
            image = flip_horiz(image)
        if args.flip_vert:
            image = flip_vert(image)
        quality = args.compression if args.compression else 100
        save_image(image, output_path, quality = quality)
    

    if args.convert:
        base, _ = os.path.splitext(args.image_path)
        output_format = args.convert.lower()
        if args.output_path:
            output_path = args.output_path
        else:
            output_path = f"{base}.{output_format}"
        if output_format == 'svg':
            import cairosvg
            cairosvg.svg2png(url = args.image_path, write_to = output_path)
        else:
            image = convert_image(image, output_format)
            image.save(output_path, format = output_format.upper())

        print(f"Image saved as {output_path}")

if __name__ == "__main__":
    main()