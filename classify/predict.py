from datetime import datetime
from PIL import Image
from torchvision import transforms
from urllib.request import urlopen

import logging
import os
import sys
import torch
import tempfile
import torchvision.models as models

useTemp = True

if 'ModelDirectory' in os.environ:
    modelDirectory = os.getenv('ModelDirectory')
    if os.path.isdir(modelDirectory):
        useTemp = False

if useTemp:
    modelDirectory = tempfile.gettempdir()

os.environ['TORCH_HOME'] = modelDirectory

if 'ModelName' in os.environ:
    modelName = os.getenv('ModelName')
else:
    modelName = 'resnet18'

#These are some of the pre-trained models from here:
#https://pytorch.org/docs/stable/torchvision/models.html

if(modelName == 'alexnet'):
    model = models.alexnet(pretrained=True, progress=False)
elif(modelName == 'resnet18'):
    model = models.resnet18(pretrained=True, progress=False)
elif(modelName == 'resnet34'):
    model = models.resnet34(pretrained=True, progress=False)
elif(modelName == 'resnet50'):
    model = models.resnet50(pretrained=True, progress=False)
elif(modelName == 'resnet101'):
    model = models.resnet101(pretrained=True, progress=False)
elif(modelName == 'resnet152'):
    model = models.resnet152(pretrained=True, progress=False)
elif(modelName == 'vgg11'):
    model = models.vgg11(pretrained=True, progress=False)
elif(modelName == 'vgg11_bn'):
    model = models.vgg11_bn(pretrained=True, progress=False)
elif(modelName == 'vgg13'):
    model = models.vgg13(pretrained=True, progress=False)
elif(modelName == 'vgg13_bn'):
    model = models.vgg13_bn(pretrained=True, progress=False)
elif(modelName == 'squeezenet1_0'):
    model = models.squeezenet1_0(pretrained=True, progress=False)
elif(modelName == 'squeezenet1_1'):
    model = models.squeezenet1_1(pretrained=True, progress=False)
elif(modelName == 'densenet161'):
    model = models.densenet161(pretrained=True, progress=False)
elif(modelName == 'shufflenet_v2_x0_5'):
    model = models.shufflenet_v2_x0_5(pretrained=True, progress=False)
elif(modelName == 'mobilenet_v2'):
    model = models.mobilenet_v2(pretrained=True, progress=False)
elif(modelName == 'mnasnet1_0'):
    model = models.mnasnet1_0(pretrained=True, progress=False)
elif(modelName == 'googlenet'):
    model = models.googlenet(pretrained=True, progress=False)

model.eval()

def get_class_labels():
    class_dict = {}
    counter = 0
    try:
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, 'labels.txt'), 'r') as infile:
            for line in infile.readlines():
                out = line.split("'")
                class_dict[counter] = out[1]
                counter += 1
    except FileNotFoundError:
        logging.info(os.listdir(os.curdir))
        logging.info(os.curdir)
        raise

    return class_dict

def predict_image_from_url(image_url):   
    logging.info('using model: ' + modelName)
    logging.info('model is loaded from ' + modelDirectory)
    class_dict = get_class_labels()
    with urlopen(image_url) as testImage:
        input_image = Image.open(testImage).convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            logging.info('Using GPU')
            input_batch = input_batch.to('cuda')
            model.to('cuda')  
        
        with torch.no_grad():
            output = model(input_batch)        
  
        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        softmax = (torch.nn.functional.softmax(output[0], dim=0))
        out = class_dict[softmax.argmax().item()]

        response = {
            'created': datetime.utcnow().isoformat(),
            'predictedTagName': out,
            'prediction': softmax.max().item(),
            'modelUsed' : modelName
        }

        logging.info(f'returning {response}')
        return response

if __name__ == '__main__':
    predict_image_from_url(sys.argv[1])
