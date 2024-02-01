import argparse
import logging
import os

import tinify

def main():

    args = cli_args()
    # use the CLI arguments to set up the app
    # configure logging
    logging.basicConfig(level=getattr(logging, args.log_level))

    # configure tinify key
    tinify.key = args.key
    if args.key == '':
        tinify.key = os.environ.get('TINYPNG_API_KEY', '')

    logging.info(f'creating output directory if it doesn\'t exist: {args.output_dir}')
    try:
        os.mkdir(args.output_dir)
    except FileExistsError:
        pass

    if args.command == 'compress':
        for input_file in args.input_files:
            compress_image(input_file, output_dir=args.output_dir)
    elif args.command == 'resize':
        for input_file in args.input_files:
            resize_image(input_file, output_dir=args.output_dir, method=args.method, width=args.width, height=args.height)
    else:
        print('Invalid command. Use "compress" or "resize".')

def cli_args():
    parser = argparse.ArgumentParser(description='Compress images for web apps using tinyPNG API')
    parser.add_argument('--key', '-k', default='', type=str, help='tiny PNG API key', required=False)
    parser.add_argument('--output-dir', '-o', default='/tmp/pynypng', type=str,
                        help='output directory to store converted images', required=False)
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO', help='Set the logging level (default: INFO)')
    parser.add_argument('--command', '-c', choices=['compress', 'resize'], default='compress',
                        help='Command to perform: compress or resize. Default is compress.')
    parser.add_argument('input_files', nargs='+', help='image files to convert')
    parser.add_argument('--width', '-w', type=int, default=150, help='Width for resizing. Required for resize command.')
    parser.add_argument('--height', '-a', type=int, default=100, help='Height for resizing. Required for resize command.')
    parser.add_argument('--method', '-m', type=str, choices=["scale", "fit", "cover", "thumb"], default="cover", help='Resize method to use. Required for resize command.')
    return parser.parse_args()

def resize_image(file_path: str, output_dir: str, method:str="cover", width:int=150, height:int=100):
     """
     Resize the given image using Tinify API.
     If file_path is a directory it recursively reads all the image files in it
     :param file_path: The path to the image file.
     :param output_dir: The directory where the compressed image will be saved.
                       Defaults to '/tmp/pynypng'.
     :param method: The resize method to use, see: https://tinypng.com/developers/reference/python
     :param width: The target width of the image
     :param height: The target height of the image
     Method reference:
     scale: Scales the image down proportionally. You must provide either a target width or a target height, but not both.
     The scaled image will have exactly the provided width or height.
     fit: Scales the image down proportionally so that it fits within the given dimensions.
     You must provide both a width and a height. The scaled image will not exceed either of these dimensions.
     cover: Scales the image proportionally and crops it if necessary so that the result has exactly the given dimensions.
     You must provide both a width and a height. Which parts of the image are cropped away is determined automatically.
     An intelligent algorithm determines the most important areas of your image.
     thumb: A more advanced implementation of cover that also detects cut out images with plain backgrounds.
     The image is scaled down to the width and height you provide. If an image is detected with a free standing object
     it will add more background space where necessary or crop the unimportant parts.
     """
     if os.path.isfile(file_path):
        logging.info(f'resizing image: {file_path}')
        source = tinify.from_file(file_path)
        resized = source.resize(method=method, width=width, height=height)
        output_file = os.path.join(output_dir, os.path.basename(file_path))
        logging.info(f'writing results to: {output_file}')
        resized.to_file(output_file)
     if os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            for file in files:
                image_file_path = os.path.join(root, file)
                resize_image(image_file_path, output_dir, method, width, height)
def compress_image(file_path: str, output_dir='/tmp/pynypng'):
    """
     Compress the given image using Tinify API.
     If file_path is a directory it recursively reads all the image files in it

     :param file_path: The path to the image file.
     :param output_dir: The directory where the compressed image will be saved.
                       Defaults to '/tmp/pynypng'.
     """
    if os.path.isfile(file_path):
        logging.info(f'parsing file: {file_path}')
        with open(file_path, 'rb') as source:
            source_data = source.read()
            result_data = tinify.from_buffer(source_data).to_buffer()
        output_file = os.path.join(output_dir, os.path.basename(file_path))
        logging.info(f'writing results to: {output_file}')
        with open(output_file, 'wb') as destination:
            destination.write(result_data)
    if os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            for file in files:
                image_file_path = os.path.join(root, file)
                compress_image(image_file_path, output_dir)

if __name__ == '__main__':
    main()







