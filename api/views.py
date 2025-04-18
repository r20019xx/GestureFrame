import pathlib

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import torch
from PIL import Image
import os

# Load YOLOv5 model globally
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # define path to projects root directory
# model_path = os.path.join(BASE_DIR, "backend_ml_model", "best.pt")      # define path to best.pt
# BASE_DIR = 'C:/Users/victo/PycharmProjects'
# model_path = 'C:/Users/victo/PycharmProjects/SignVisionAI-Front-End/backend_ml_model/best.pt'
# # use pytorch to load yolov5 model
# model = torch.hub.load(
#     #os.path.join(BASE_DIR, "backend_ml_model", "yolov5"),
#     'C:/Users/victo/PycharmProjects/SignVisionAI-Front-End/backend_ml_model/yolov5',
#     "custom",
#     path=model_path,
#     source="local",
#     force_reload=True
# )

pathlib.PosixPath = pathlib.WindowsPath

# Load the custom-trained YOLOv5 model from a local file ('best.pt')
model = torch.hub.load('yolov5', 'custom', path='C:/Users/victo/PycharmProjects/SignVisionAI-Front-End/backend_ml_model/best.pt', source='local')


# An APIView class that's used for incorporating yolov5 model image prediction with script.json for upload webpage
class PredictView(APIView):
    parser_classes = (MultiPartParser, FormParser)  #parser will receive image files
    # get image "file" from upload webpage process in page/static/script.js sendToBackend() .
    def post(self, request, format=None):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)  # if no file uploaded. 400: Bad request

        try:
            image = Image.open(file).convert("RGB")     # try to upload image "file"
            results = model(image)                      # get images from yolov5 ml model
            detections = results.xyxy[0]                # detected raw prediction results from model
            # put model output into a list to be shown in upload webpage.
            output = []
            # break down the prediction results and put into output list
            for *box, conf, cls in detections:
                x1, y1, x2, y2 = map(int, box)
                class_name = model.names[int(cls)].strip("?")
                label = f"{class_name}: {conf:.2f}"
                output.append({
                    "label": label,
                    "x1": x1,   # box coordinates x1, y1, x2, y2
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "confidence": float(conf),  # confidence score
                    "class_name": class_name    # Predicted ASL sign
                })

            return Response({"predictions": output})
        # Handle any errors with results yolov5 prediction model
        except Exception as e:
            return Response({"error": str(e)}, status=500)  #server error
