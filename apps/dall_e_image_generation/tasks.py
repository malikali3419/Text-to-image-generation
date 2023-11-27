from celery import shared_task
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os
import logging
import re

class ImageGenerator:
    def __init__(self) -> None:
        load_dotenv()

        SECRET_KEY = os.getenv('SECRET_KEY')
        ORGANIZATION_KEY = os.getenv('ORG_KEY')
        self.client = OpenAI(api_key=SECRET_KEY,organization=ORGANIZATION_KEY)

    def get_image(self,prompt:str)->str:
        """This function actake a prompt of image to be generated and sends the prompt to DALL-E 3 which then returns a url of the 
            generated image.
           args:
                prompt (str): contains the information of what you want the image to look like.  
           returns:
                image_url(str)
        """
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url

def sanitize_filename(name:str) -> str:
    """Sanitize the filename to remove non-alphanumeric characters and limit length."""
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return sanitized[:100]

def create_directory(directory_name:str) -> None:
    """Create a directory if it does not exist."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name, exist_ok=True)
    return

def save_image(prompt: str, image_url: str, directory: str = "generated_images") -> bool:
    """
    Downloads an image from the given URL and saves it to a file within a specified directory.

    The filename is derived from the prompt, sanitized, and truncated to 100 characters.
    The directory is created if it does not exist.

    Args:
        prompt (str): The text prompt used to generate the image.
        image_url (str): The URL of the image to download.
        directory (str): The directory where the image will be saved.

    Returns:
        bool: True if the image was downloaded and saved successfully, False otherwise.
    """

    try:
        # Ensure the directory exists
        create_directory(directory)

        response = requests.get(image_url, timeout=10)

        if response.status_code == 200:
            filename = os.path.join(directory, sanitize_filename(prompt) + '.png')
            with open(filename, 'wb') as file:
                file.write(response.content)
            logging.info(f"Image downloaded and saved as {filename}")
            return True
        else:
            logging.error(f"Failed to download the image. HTTP status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        logging.error(f"Error occurred while downloading the image: {e}")
        return False
    
@shared_task
def generate_image(prompt:str) -> None:
    obj = ImageGenerator()
    image_url = obj.get_image(prompt)
    save_image(prompt=prompt,image_url=image_url)
    print(f"\n\n{image_url}")
    return
