try:
    import unzip_requirements
except ImportError:
    pass
import io
import os
import time

import boto3
import requests
import torch
from PIL import Image
from torchvision import transforms

s3_resource = boto3.resource('s3')

img_tranforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])


def download_image(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            f = io.BytesIO(r.content)
            img = Image.open(f)
            return img
        else:
            return None
    except:
        return None


def download_model(bucket='', key=''):
    location = f'/tmp/{os.path.basename(key)}'
    if not os.path.exists(location):
        s3_resource.Object(bucket, key).download_file(location)
    return location


def classify_image(model_path, img):
    model = torch.jit.load(model_path)
    img = img_tranforms(img).unsqueeze(0)
    cl = model(img).argmax().item()
    return cl


def lambda_handler(event, context):
    # download model
    model_path = download_model(
        bucket='segmentsai-dl', key='models/pytorch_model.pt')
    # download image
    img = download_image(event['url'])
    # classify image
    if img:
        cl = classify_image(model_path, img)
        return {
            'statusCode': 200,
            'class': cl
        }
    else:
        return {
            'statusCode': 404,
            'class': None
        }