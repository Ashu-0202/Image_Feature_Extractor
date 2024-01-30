import head_segmentation.segmentation_pipeline as seg_pipeline
import cv2
import numpy as np
from PIL import Image

def segment_head(input_image_path, output_image_path):
    segmentation_pipeline = seg_pipeline.HumanHeadSegmentationPipeline()
    
    image = np.asarray(Image.open(input_image_path))
    if image.shape[-1] > 3:
        image = image[..., :3]

    segmentation_map = segmentation_pipeline.predict(image)

    segmented_region = image * cv2.cvtColor(segmentation_map, cv2.COLOR_GRAY2BGR)
    pil_image = Image.fromarray(segmented_region)
    pil_image.save(output_image_path)
    