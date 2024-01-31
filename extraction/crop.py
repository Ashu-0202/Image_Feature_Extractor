''' This code is designed to extract the facial region from an image, 
 resulting in an image focused specifically on the face. '''

from PIL import Image
from extraction import FaceRegionExtractor
from resize_and_segmentation import AvatarMaker

class crop_image():
    def __init__(self, small_image_path):
        self.image_path = small_image_path
        self.image = None
        self.AvatarMaker_obj = AvatarMaker(small_image_path)

    def check_orientation(self): # vertical body in image ....
        if hasattr(self.image, '_getexif'):
            exif = self.image._getexif()
            if exif is not None and 0x0112 in exif:
                orientation = exif[0x0112]
                if orientation == 3:
                    self.image = self.image.rotate(180, expand=True)
                elif orientation == 6:
                    self.image = self.image.rotate(270, expand=True)
                elif orientation == 8:
                    self.image = self.image.rotate(90, expand=True)
    
    def crop(self, cropped_image_path):
        self.image = Image.open(self.image_path)
        self.check_orientation() # check orientation first
        
        FaceRegionExtractor_obj = FaceRegionExtractor(face_image_path=self.image_path)
        dlib_facelandmark, faces, gray = FaceRegionExtractor_obj.get_attributes()
        
        for face in faces:
            face_landmarks = dlib_facelandmark(gray, face)
            
            #  perform crop operation ( use heiuristic accoring to use case)
            ''' For sprite images as yet to finalise on a proper heiuristic'''
            # cropped_image = self.image.crop((face_landmarks.part(0).x - 80, 0,
            #                                 face_landmarks.part(0).x + 176, 210))
            '''For normal image with one face only ..... '''
            cropped_image = self.image.crop((max(0,face_landmarks.part(0).x - 1000), max(0,face_landmarks.part(19).y - 800),
                                 min(face_landmarks.part(16).x + 1000, self.image.size[0]), min(face_landmarks.part(8).y + 500, self.image.size[1])))
            cropped_image.save(cropped_image_path)
            
