from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.dall_e_image_generation.tasks import generate_image
import logging

logging.basicConfig(filename='activity_log.log', level=logging.INFO)
class ImageGenerationView(APIView):
    """
    This view handles POST requests to initiate image generation tasks based on provided prompts.

    The view accepts a list of prompts in the request body and enqueues each prompt for asynchronous 
    processing using Celery tasks.
    """

    def post(self, request):
        prompts = request.data.get("prompts", [])

        if not isinstance(prompts, list) or not all(isinstance(prompt, str) for prompt in prompts):
            logging.error("Invalid input: Prompts should be a list of strings.")
            return Response({"error": "Invalid input. Prompts should be a list of strings."},
                            status=status.HTTP_400_BAD_REQUEST)

        for prompt in prompts:
            try:
                generate_image.delay(prompt)
            except Exception as e:
                logging.error(f"Error enqueuing image generation task for prompt '{prompt}': {e}")
        
        return Response({"status": "Accepted"}, status=status.HTTP_202_ACCEPTED)
