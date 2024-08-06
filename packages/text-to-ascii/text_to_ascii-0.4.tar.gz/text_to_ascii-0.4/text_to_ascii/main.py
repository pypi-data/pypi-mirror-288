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
    return cv2.resize(image, (new_w, new_h))


def count_black_pixels(image, threshold):
    return np.sum(image <= threshold)


# Fills in the text until the length fits the image if the text does not fit exactly
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


def text_to_ascii(text_path, image_path, copies, filler, threshold):
    with open(text_path, "r") as file:
        text = ' '.join(line.rstrip() for line in file)

    text = text * copies
    text_length = len(text)
    img = cv2.imread(image_path, 0)

    if img is None:
        raise FileNotFoundError(f"Image file {image_path} not found.")

    resized_image = rescale_image_to_fit(img, text_length, threshold)
    black_pixel_count = count_black_pixels(resized_image, threshold)

    text = fill_text(text, black_pixel_count, filler)
    print(print_text_on_image(resized_image, text, threshold))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("text_path", help="Text to be formatted")
    parser.add_argument("image_path", help="Image to format the text into")
    parser.add_argument("-c", "--copies", type=int, default=1, help="Amount of copies of the text")
    parser.add_argument("-f", "--filler", default=" ", help="Character to fill extra spaces")
    parser.add_argument("-t", "--threshold", type=int, default=220, help="Threshold to identify black pixels")

    args = parser.parse_args()
    text_to_ascii(args.text_path, args.image_path, args.copies, args.filler, args.threshold)


if __name__ == "__main__":
    main()
