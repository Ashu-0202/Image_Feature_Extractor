import numpy as np
import cv2, os
from resize_and_segmentation import AvatarMaker
from change_background_to_none import change_background
from extraction import FaceRegionExtractor

class image_processor:
    def __init__(self, input_image_path):
        self.input_image_path = input_image_path
        self.small_image_path = self.input_image_path.split('.png')[0] + '_small.png'
        self.final_path = self.input_image_path.split('.png')[0] + '_face.png'
        self.cropped_path = self.input_image_path.split('.png')[0] + '_cropped.png'

        self.AvatarMaker_obj = AvatarMaker(input_image_path)

    def process_image(self, small_image_dimensions = None):
        image = cv2.imread(self.input_image_path)
        if small_image_dimensions == None:
            small_image_dimensions = image.shape[:2]

        s_height, s_width = small_image_dimensions
        i_height, i_width, i_depth = image.shape
        blank_sprite = np.zeros((i_height, i_width, i_depth), dtype=np.uint8) 

        for width in range(0, i_width - s_width + 1, s_width):
            for height in range(0, i_height - s_height + 1, s_height):
                small_image = image[height: height+s_height, width: width+s_width, :]
                cv2.imwrite(self.small_image_path, small_image)
                
                self.AvatarMaker_obj.generate_avatar_components()   
                blank_sprite[height: height+s_height, width: width+s_width, :] = cv2.imread(self.small_image_path)
            
        cv2.imwrite(self.final_path, blank_sprite)
        change_background(self.final_path)
        
        FaceRegionExtractor_obj = FaceRegionExtractor(self.input_image_path, self.final_path)
        FaceRegionExtractor_obj.extract_regions()
            
        os.remove(self.small_image_path)