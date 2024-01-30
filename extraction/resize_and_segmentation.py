from PIL import Image
from segment_out_head import segment_head
import os
from change_background_to_none import change_background

class AvatarMaker :
    def __init__(self, input_image_path):
        # paths ....
        self.image_path = input_image_path
        self.final_path = input_image_path.split('.png')[0] + '_small.png' 
        self.resized_path = input_image_path.split('.png')[0] + '_resized.png'
        self.celebA_path = input_image_path.split('.png')[0] + '_celebA.png'
        
        # get sizes and calculate aspect ratios ....
        self.original_image = None
        self.target_size = [178, 218]

    # Crop to size of celebA dataset ....
    def resize_image(self):
        self.original_image = Image.open(self.final_path)
        
        original_aspect_ratio = self.original_image.size[0] / self.original_image.size[1]
        target_aspect_ratio = self.target_size[0] / self.target_size[1]

        if original_aspect_ratio > target_aspect_ratio :
            new_width = int(self.target_size[1] * original_aspect_ratio)
            new_height = self.target_size[1]
        else:
            new_width = self.target_size[0]
            new_height = int(self.target_size[0] / original_aspect_ratio)
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        left = (resized_image.width - self.target_size[0]) / 2
        top = (resized_image.height - self.target_size[1]) / 2
        right = (resized_image.width + self.target_size[0]) / 2
        bottom = (resized_image.height + self.target_size[1]) / 2

        resized_image = resized_image.crop((left, top, right, bottom))
        resized_image.save(self.resized_path)
    
    # Crop back to original size of image passed ....
    def reverse_resize_image(self):
        resized_image = Image.open(self.celebA_path)
        resized_width, resized_height = resized_image.size
        resized_aspect_ratio = resized_width / resized_height

        # Calculate the target size based on the original aspect ratio
        if self.original_image.size[0]/self.original_image.size[1] > resized_aspect_ratio:
            target_width_reverse = int(self.original_image.size[1] * resized_aspect_ratio)
            target_height_reverse = self.original_image.size[1]
        else:
            target_width_reverse = self.original_image.size[0]
            target_height_reverse = int(self.original_image.size[0] / resized_aspect_ratio)

        # Resize the resized image back to the target size
        resized_image_reverse = resized_image.resize((target_width_reverse, target_height_reverse), Image.Resampling.LANCZOS)

        # Calculate the coordinates for cropping the image to the original size
        left_reverse = (resized_image_reverse.width - self.original_image.size[0]) / 2
        top_reverse = (resized_image_reverse.height - self.original_image.size[1]) / 2
        right_reverse = (resized_image_reverse.width + self.original_image.size[0]) / 2
        bottom_reverse = (resized_image_reverse.height + self.original_image.size[1]) / 2

        # Crop the image to the original size
        restored_image = resized_image_reverse.crop((left_reverse, top_reverse, right_reverse, bottom_reverse))
        restored_image.save(self.final_path)
        
    def generate_avatar_components(self):
        # crop to celebA size
        self.resize_image()
        # perform head segmentaion    
        segment_head(self.resized_path, self.celebA_path)
        change_background(self.celebA_path)
        # reverse crop
        self.reverse_resize_image()
        os.remove(self.celebA_path)
        os.remove(self.resized_path)


