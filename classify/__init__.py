import logging
import azure.functions as func
import json

# Import helper script
from .predict import predict_image_from_url


def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('img')
    model = req.params.get('model')
    logging.info('Image URL received: ' + image_url)    
    results = predict_image_from_url(image_url)

    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(json.dumps(results), headers = headers)
