# Text to Image Generation

This Django project allows you to generate images based on text prompts using the DALL-E model. It utilizes Celery for asynchronous task processing.

## Getting Started

### Prerequisites

- Python 3.8.0
- Django
- Celery
- Redis (as Celery broker)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/malikali3419/Text-to-image-generation.git
    cd Text-to-image-generation/
    ```

2. Create a new Virtual Environment:

    ```bash
   python -m venv env
    ```
   
3. Activate Virtual Environment:

    ```bash
   source env/bin/activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up your environment variables:

    Create a `.env` file in the project root with the following content:

    ```dotenv
    SECRET_KEY="your_secret_key"
    ORG_KEY="your_organization_key"
    # Add any other environment variables specific to your project
    ```

6. Apply migrations:

    ```bash
    python manage.py migrate
    ```

7. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

8. Start the Celery worker:

    ```bash
    celery -A image_generation worker --loglevel=info
    ```

9.  Send a POST request to the image generation endpoint:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"prompts": ["Your text prompt here"]}' http://localhost:8000/api/strings/
    ```
After calling the endpoint, the generated images will be stored in the `generated_images` folder within the project directory.

