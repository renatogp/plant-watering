import io
import logging
import os
import sys
import time
from datetime import datetime
from picamera import PiCamera

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored/'))

import boto3

import greengrasssdk

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Initializing Camera/handler')

S3_BUCKET_NAME = 'plant-watering-images'
INTERVAL = 600 # seconds -> 10 min

def capture_image():
    """
    Captures image from RPi Camera
    """
    logger.info('Invoked function capture_image()')

    image_stream = io.BytesIO()
    camera = PiCamera()

    camera.start_preview()
    time.sleep(2) # camera warm-up time
    camera.capture(image_stream, 'jpeg')

    file_name = '{}.jpg'.format(datetime.now().isoformat().replace(':', ''))

    logger.info('Image captured, transferring to s3://{}/{}'.format(
        S3_BUCKET_NAME,
        file_name,
    ))

    s3 = boto3.client('s3')

    image_stream.seek(0)
    s3.upload_fileobj(image_stream, S3_BUCKET_NAME, file_name)

    return


def start():
    while True:
        capture_image()
        time.sleep(INTERVAL)

start()

def pinned_handler():
    """
    Mock function to run pinned lambda
    """
    pass