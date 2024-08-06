# main.py
import cv2
import numpy as np
import math
import random
import argparse


# Increment scale of the image until it properly fits the text
def rescale_image_to_fit(image, text_length, threshold):
    h, w = image.shape
    original_black_pixel_count = count_black_pixels(image, threshold)
    required_scale = (text_length / original_black_pixel_count) ** 0.5
    new_h = math.ceil(h * required_scale)
    new_w = math.ceil(w * required_scale)
    return cv2.resize(image, (new_w, new_h)), required_scale

def count_black_pixels(image, threshold):
    return np.sum(image <= threshold)

# Fills in the text until the length fits the image if the text does not fit exactly (slightly less than the image)
def fill_text(text, target_length, filler):
    if not filler:
        raise Exception("Filler cannot be empty string")

    while len(text) < target_length:
        rand_indx = random.randint(1, len(text))
        text = text[:rand_indx] + filler + text[rand_indx:]
    return text


def print_text_on_image(image, text, threshold):
    text_indx = 0
    output = ""
    for row in image:
        for col in row:
            if col > threshold:
                output += "  "
            else:
                output += text[text_indx] + " "
                text_indx += 1
        output += "\n"
    return output


def text_to_ascii(text, image_path, multiplier, filler, threshold):
    text = text * multiplier
    text_length = len(text)
    img = cv2.imread(image_path, 0)

    resized_image, scale = rescale_image_to_fit(img, text_length, threshold)
    black_pixel_count = count_black_pixels(resized_image, threshold)
    text = fill_text(text, black_pixel_count, filler)
    print(print_text_on_image(resized_image, text, threshold))

    print(f"Scale applied to original image: {round(scale, 4)}")
    print(f"Character size of image: {black_pixel_count}\nCharacter size of text: {text_length}")
    print(f"Filled in image with {black_pixel_count - text_length} filler characters ('{filler}')")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("text", help="Text to be formatted")
    parser.add_argument("image_path", help="Image to format the text into")
    parser.add_argument("-m", type=int, default=1, help="Value of repetitions of the text")
    parser.add_argument("-filler", default=" ", help="Character to fill extra spaces")
    parser.add_argument("-threshold", type=int, default=220, help="Threshold [0-254] to identify black pixels")

    args = parser.parse_args()
    text_to_ascii(args.text, args.image_path, args.m, args.filler, args.threshold)

if __name__ == "__main__":
    main()
