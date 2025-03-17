import io
from PIL import Image
import pandas as pd
import numpy as np

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

# import torch

# _old_load = torch.load
# torch.load = lambda f, map_location=None, **kwargs: _old_load(
#     f, map_location=map_location, weights_only=False, **kwargs
# )


model_sample_model = YOLO("./../best.pt")


def transform_predict_to_df(results: list, labeles_dict: dict) -> pd.DataFrame:
    predict_bbox = pd.DataFrame(
        results[0].to("cpu").numpy().boxes.xyxy,
        columns=["xmin", "ymin", "xmax", "ymax"],
    )
    predict_bbox["confidence"] = results[0].to("cpu").numpy().boxes.conf
    predict_bbox["class"] = (results[0].to("cpu").numpy().boxes.cls).astype(int)
    predict_bbox["name"] = predict_bbox["class"].replace(labeles_dict)
    return predict_bbox


def get_model_predict(
    model: YOLO,
    input_image: Image,
    save: bool = False,
    image_size: int = 1248,
    conf: float = 0.5,
    augment: bool = False,
) -> pd.DataFrame:
    predictions = model.predict(
        imgsz=image_size,
        source=input_image,
        conf=conf,
        save=save,
        augment=augment,
        flipud=0.0,
        fliplr=0.0,
        mosaic=0.0,
    )

    predictions = transform_predict_to_df(predictions, model.model.names)
    return predictions


def detect_sample_model(input_image: Image) -> pd.DataFrame:
    """
    Predict from sample_model.
    Base on YoloV8

    Args:
        input_image (Image): The input image.

    Returns:
        pd.DataFrame: DataFrame containing the object location.
    """
    predict = get_model_predict(
        model=model_sample_model,
        input_image=input_image,
        save=False,
        image_size=640,
        augment=False,
        conf=0.5,
    )
    return predict


def add_bboxs_on_img(image: Image, predict: pd.DataFrame()) -> Image:
    annotator = Annotator(np.array(image), font_size=40, pil=True)

    predict = predict.sort_values(by=["xmin"], ascending=True)

    for i, row in predict.iterrows():
        text = f"{row['name']}: {int(row['confidence'] * 100)}%"
        bbox = [row["xmin"], row["ymin"], row["xmax"], row["ymax"]]
        annotator.box_label(bbox, text, color=colors(row["class"], True))
    return Image.fromarray(annotator.result())


def get_bytes_from_image(image: Image) -> bytes:
    return_image = io.BytesIO()
    image.save(return_image, format="JPEG", quality=85)
    return_image.seek(0)
    return return_image


def get_image_from_bytes(binary_image: bytes) -> Image:
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image
