import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Flux3DevAPI:
    def __init__(self, api_key=None):
        """
        Initialize the FLUX 3 Dev API client.
        :param api_key: Your MuAPI.ai API key. Defaults to MUAPI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Set MUAPI_API_KEY in .env or pass it to the constructor.")

        self.base_url = "https://api.muapi.ai/api/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def generate(self, prompt, aspect_ratio="1:1", resolution="1k"):
        """
        Submits a FLUX 3 Dev text-to-image generation task.

        FLUX 3 Dev is the faster, lower-cost variant of Black Forest Labs' FLUX 3
        frontier model — ideal for rapid iteration, prototyping, and high-volume
        generation, with a planned open-weight release later in 2026.

        :param prompt: Text prompt describing the image.
        :param aspect_ratio: Output aspect ratio (e.g. '16:9', '9:16', '1:1', '4:3', '3:4', '2:3', '3:2', '21:9').
        :param resolution: Output resolution ('1k', '2k', or '4k').
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/flux-3-dev"
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }
        return self._post_request(endpoint, payload)

    # ------------------------------------------------------------------
    # Sibling FLUX 3 endpoints (same family, different variants)
    # ------------------------------------------------------------------

    def text_to_image(self, prompt, aspect_ratio="1:1", resolution="2k"):
        """
        Submits a FLUX 3 (flagship) Text-to-Image generation task.

        Higher fidelity than FLUX 3 Dev — use this when quality matters more
        than latency or cost.

        :param prompt: Text prompt describing the image.
        :param aspect_ratio: Output aspect ratio.
        :param resolution: Output resolution ('1k', '2k', or '4k').
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/flux-3-text-to-image"
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }
        return self._post_request(endpoint, payload)

    def image_to_image(self, prompt, images_list, aspect_ratio="1:1", resolution="2k"):
        """
        Submits a FLUX 3 Image-to-Image (edit) task.

        Edit or restyle an existing image using a text instruction plus up to
        4 reference images, preserving subject identity and scene structure.

        :param prompt: Edit instruction describing the desired change.
        :param images_list: List of up to 4 reference image URLs.
        :param aspect_ratio: Output aspect ratio.
        :param resolution: Output resolution ('1k', '2k', or '4k').
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/flux-3-image-to-image"
        payload = {
            "prompt": prompt,
            "images_list": images_list,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }
        return self._post_request(endpoint, payload)

    def text_to_video(self, prompt, aspect_ratio="16:9", resolution="720p", duration=5, generate_audio=True):
        """
        Submits a FLUX 3 Text-to-Video generation task.

        Generates a cinematic video clip with optional native synchronized
        audio from a single unified model.

        :param prompt: Text prompt describing the video scene and motion.
        :param aspect_ratio: Output aspect ratio.
        :param resolution: Output resolution ('480p', '720p', or '1080p').
        :param duration: Video duration in seconds (4-10).
        :param generate_audio: Whether to generate synchronized native audio.
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/flux-3-text-to-video"
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration": duration,
            "generate_audio": generate_audio,
        }
        return self._post_request(endpoint, payload)

    def image_to_video(self, prompt, images_list, aspect_ratio="16:9", resolution="720p", duration=5, generate_audio=True):
        """
        Submits a FLUX 3 Image-to-Video generation task.

        Animates a still image into a cinematic clip with optional native
        synchronized audio, keeping motion physically consistent with the
        source frame.

        :param prompt: Text prompt describing the desired motion.
        :param images_list: List containing the start-frame image URL.
        :param aspect_ratio: Output aspect ratio.
        :param resolution: Output resolution ('480p', '720p', or '1080p').
        :param duration: Video duration in seconds (4-10).
        :param generate_audio: Whether to generate synchronized native audio.
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/flux-3-image-to-video"
        payload = {
            "prompt": prompt,
            "images_list": images_list,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration": duration,
            "generate_audio": generate_audio,
        }
        return self._post_request(endpoint, payload)

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _post_request(self, endpoint, payload):
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def upload_file(self, file_path):
        """
        Uploads a file (image or video) to MuAPI for use in generation tasks.

        :param file_path: Path to the local file to upload.
        :return: JSON response from MuAPI containing the URL of the uploaded file.
        """
        endpoint = f"{self.base_url}/upload_file"

        # Omit Content-Type to let requests set the multipart boundary automatically
        headers = {
            "x-api-key": self.api_key
        }

        with open(file_path, "rb") as file_data:
            files = {"file": file_data}
            response = requests.post(endpoint, headers=headers, files=files)

        response.raise_for_status()
        return response.json()

    def get_result(self, request_id):
        """
        Polls for the result of a generation task.
        """
        endpoint = f"{self.base_url}/predictions/{request_id}/result"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, request_id, poll_interval=5, timeout=300):
        """
        Waits for the generation task to complete and returns the result.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.get_result(request_id)
            status = result.get("status")

            if status == "completed":
                return result
            elif status == "failed":
                raise Exception(f"Generation failed: {result.get('error')}")

            print(f"Status: {status}. Waiting {poll_interval} seconds...")
            time.sleep(poll_interval)

        raise TimeoutError("Timed out waiting for generation to complete.")


if __name__ == "__main__":
    # Example usage for FLUX 3 Dev text-to-image
    try:
        api = Flux3DevAPI()
        prompt = "A minimalist product shot of a ceramic mug on a wooden table, soft natural light"

        print(f"Submitting FLUX 3 Dev task with prompt: {prompt}")
        submission = api.generate(prompt=prompt, aspect_ratio="1:1", resolution="1k")
        request_id = submission.get("request_id")
        print(f"Task submitted. Request ID: {request_id}")

        print("Waiting for completion...")
        result = api.wait_for_completion(request_id)
        print(f"Generation completed! Output: {result.get('outputs', [result.get('url')])}")

    except Exception as e:
        print(f"Error: {e}")
