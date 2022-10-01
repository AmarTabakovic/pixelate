from PIL import Image, UnidentifiedImageError
import argparse

PROGRAM_NAME = 'pixelate'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from_path',
                        help='Path to the original image.',
                        type=str,
                        required=True)
    parser.add_argument('--to_path',
                        help='Path to save the new image to.',
                        type=str,
                        required=True)
    parser.add_argument('--square_size',
                        help='Size of a single square in pixels.',
                        type=int,
                        required=True)
    args = parser.parse_args()

    original_image = None

    try:
        original_image = Image.open(args.from_path)
    except FileNotFoundError:
        print(f'{PROGRAM_NAME}: File was not found.')
        exit(1)
    except UnidentifiedImageError:
        print(f'{PROGRAM_NAME}: Could not identify image file.')
        exit(1)

    square_size = args.square_size
    square_size_squared = square_size * square_size

    # Square size cannot exceed the original image width or height.
    if square_size > original_image.width or square_size > original_image.height:
        print(f'{PROGRAM_NAME}: Square size is too big.')
        exit(1)

    # Crop the original image down to a multiple of the size of a single pixelate square.
    cropped_width = original_image.width - (original_image.width %
                                            square_size)
    cropped_height = original_image.height - (original_image.height %
                                              square_size)

    original_image.crop((0, 0, cropped_width, cropped_height))
    original_image = original_image.convert('RGB')

    pixelated_image = Image.new('RGB', size=(cropped_width, cropped_height))

    for i in range(0, cropped_height, square_size):
        for j in range(0, cropped_width, square_size):
            # Compute the average RGB value in each pixelate square section.
            average_r = 0
            average_g = 0
            average_b = 0

            for y in range(i, i + square_size):
                for x in range(j, j + square_size):
                    r, g, b = original_image.getpixel((x, y))
                    average_r += r
                    average_g += g
                    average_b += b

            average_r //= square_size_squared
            average_g //= square_size_squared
            average_b //= square_size_squared

            # TODO: Draw a rectangle instead of drawing each pixel maybe?
            for y in range(i, i + square_size):
                for x in range(j, j + square_size):
                    pixelated_image.putpixel((x, y),
                                             (average_r, average_g, average_b))

    pixelated_image.save(args.to_path)


if __name__ == '__main__':
    main()
