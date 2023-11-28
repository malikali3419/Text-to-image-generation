import logging
import os
import re

import requests
from celery import shared_task
from openai import OpenAI

from image_generation.settings import SECRET_KEY, ORGANIZATION_KEY


class ImageGenerator:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=SECRET_KEY, organization=ORGANIZATION_KEY)

    def get_image(self, prompt: str) -> str:
        """
        This function takes a prompt of image to be generated and sends the prompt to DALL-E 3 which then returns a url of the
            generated image.

        Args:
            prompt (str): contains the information of what you want the image to look like.

        Return:
            image_url(str)
        """
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # Extract the image URL from the response
        image_url = response.data[0].url
        return image_url


def clip_filename(name: str) -> str:
    """
    Sanitize the filename to remove non-alphanumeric characters and limit length.

    Args:
        name (str): The input filename.

    Return:
        cliped_filename (str): The sanitized and clipped filename.
    """
    cliped_filename = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return cliped_filename[:100]


def create_directory(directory_name: str) -> None:
    """
    Create a directory if it does not exist.

    Args:
        directory_name (str): The name of the directory to be created.

    Return:
        None
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name, exist_ok=True)


def save_image(prompt: str, image_url: str, directory: str = "generated_images") -> bool:
    """
    Downloads an image from the given URL and saves it to a file within a specified directory.

    The filename is derived from the prompt, sanitized, and truncated to 100 characters.
    The directory is created if it does not exist.

    Args:
        prompt (str): The text prompt used to generate the image.
        image_url (str): The URL of the image to download.
        directory (str): The directory where the image will be saved.

    Return:
        bool: True if the image was downloaded and saved successfully, False otherwise.
    """

    try:
        # Ensure the directory exists
        create_directory(directory)

        response = requests.get(image_url, timeout=10)

        if response.status_code == 200:
            filename = os.path.join(directory, clip_filename(prompt) + '.png')
            with open(filename, 'wb') as file:
                file.write(response.content)
            logging.info(f"Image downloaded and saved as {filename}")
            return True
        logging.error(f"Failed to download the image. HTTP status code: {response.status_code}")

    except Exception as e:
        logging.error(f"Error occurred while downloading the image: {e}")
        return False


@shared_task
def generate_image(prompt: str) -> None:
    """
    Generate an image based on the provided prompt and save it.

    Args:
        prompt (str): The prompt or text used to generate the image.

    Return:
        None
    """
    obj = ImageGenerator()
    image_url = obj.get_image(prompt)
    save_image(prompt=prompt, image_url=image_url)
    return
