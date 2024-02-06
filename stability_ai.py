import io
import os
import warnings
import random

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# insert your own STABILITY_KEY
# site to obtain STABILITY_KEY: https://platform.stability.ai/account/keys
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = 'sk-eEs9jKDjqFwz7hs0b5gzp1wBI8FqPuXYN18bTb9R95uyv6mr'

# set random seed
seed = random.randint(0, 1000000000)

# Set up our connection to API
stability_api = client.StabilityInference(key=os.environ['STABILITY_KEY'], verbose=True, engine="stable-diffusion-xl-1024-v1-0")

def generateImageFromText(prompt):
    # Set up our initial generation parameters.
    result = stability_api.generate(
        prompt=prompt,
        seed=seed,
        steps=30,
        cfg_scale=8.0,
        width=1024,
        height=1024,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    for response in result:
        for artifact in response.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                global image
                image = Image.open(io.BytesIO(artifact.binary))
                return image
