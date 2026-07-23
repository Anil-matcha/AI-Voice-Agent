import json
from mcp.server.fastmcp import FastMCP
from flux3_dev_api import Flux3DevAPI

# Initialize FastMCP server
mcp = FastMCP("FLUX 3 Dev API Server")

# Helper to get API client
def get_api():
    return Flux3DevAPI()

@mcp.tool()
def generate(prompt: str, aspect_ratio: str = "1:1", resolution: str = "1k") -> str:
    """
    Generate an image using FLUX 3 Dev — the faster, lower-cost FLUX 3 variant.

    :param prompt: Text prompt describing the image.
    :param aspect_ratio: Output aspect ratio (e.g. '16:9', '9:16', '1:1').
    :param resolution: Output resolution ('1k', '2k', or '4k').
    """
    api = get_api()
    result = api.generate(prompt, aspect_ratio, resolution)
    return json.dumps(result, indent=2)

@mcp.tool()
def text_to_image(prompt: str, aspect_ratio: str = "1:1", resolution: str = "2k") -> str:
    """
    Generate an image using the flagship FLUX 3 model (higher fidelity than Dev).

    :param prompt: Text prompt describing the image.
    :param aspect_ratio: Output aspect ratio.
    :param resolution: Output resolution ('1k', '2k', or '4k').
    """
    api = get_api()
    result = api.text_to_image(prompt, aspect_ratio, resolution)
    return json.dumps(result, indent=2)

@mcp.tool()
def image_to_image(prompt: str, images_list: list[str], aspect_ratio: str = "1:1", resolution: str = "2k") -> str:
    """
    Edit or restyle an existing image with FLUX 3 Image-to-Image.

    :param prompt: Edit instruction describing the desired change.
    :param images_list: List of up to 4 reference image URLs.
    :param aspect_ratio: Output aspect ratio.
    :param resolution: Output resolution ('1k', '2k', or '4k').
    """
    api = get_api()
    result = api.image_to_image(prompt, images_list, aspect_ratio, resolution)
    return json.dumps(result, indent=2)

@mcp.tool()
def text_to_video(prompt: str, aspect_ratio: str = "16:9", resolution: str = "720p", duration: int = 5, generate_audio: bool = True) -> str:
    """
    Generate a video with optional native audio using FLUX 3 Text-to-Video.

    :param prompt: Text prompt describing the video scene and motion.
    :param aspect_ratio: Output aspect ratio.
    :param resolution: Output resolution ('480p', '720p', or '1080p').
    :param duration: Video duration in seconds (4-10).
    :param generate_audio: Whether to generate synchronized native audio.
    """
    api = get_api()
    result = api.text_to_video(prompt, aspect_ratio, resolution, duration, generate_audio)
    return json.dumps(result, indent=2)

@mcp.tool()
def image_to_video(prompt: str, images_list: list[str], aspect_ratio: str = "16:9", resolution: str = "720p", duration: int = 5, generate_audio: bool = True) -> str:
    """
    Animate a still image into video with optional native audio using FLUX 3 Image-to-Video.

    :param prompt: Text prompt describing the desired motion.
    :param images_list: List containing the start-frame image URL.
    :param aspect_ratio: Output aspect ratio.
    :param resolution: Output resolution ('480p', '720p', or '1080p').
    :param duration: Video duration in seconds (4-10).
    :param generate_audio: Whether to generate synchronized native audio.
    """
    api = get_api()
    result = api.image_to_video(prompt, images_list, aspect_ratio, resolution, duration, generate_audio)
    return json.dumps(result, indent=2)

@mcp.tool()
def upload_file(file_path: str) -> str:
    """
    Upload a local file (image or video) to MuAPI for use in generation tasks.

    :param file_path: Local path to the file.
    """
    api = get_api()
    result = api.upload_file(file_path)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_task_status(request_id: str) -> str:
    """
    Check the status and get results of a generation task.

    :param request_id: The ID returned from a generation tool call.
    """
    api = get_api()
    result = api.get_result(request_id)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
