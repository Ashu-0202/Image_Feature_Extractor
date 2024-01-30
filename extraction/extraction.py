import cv2
import dlib
import numpy as np
from change_background_to_none import change_background
from PIL import Image

class FaceRegionExtractor:
    def __init__(self, whole_image_path, face_image_path):
        # reading images ...
        self.whole_image_path = whole_image_path
        self.face_image_path = face_image_path
        self.whole_image = cv2.imread(whole_image_path)
        self.face_image = cv2.imread(face_image_path)
        self.gray = cv2.cvtColor(self.face_image, cv2.COLOR_BGR2GRAY)
        
        # initialising 68 point model ....
        self.hog_face_detector = dlib.get_frontal_face_detector()
        self.dlib_facelandmark = dlib.shape_predictor("../models/shape_predictor_68_face_landmarks.dat")
        
        # used to get output ....
        self.output_image = [np.zeros_like(self.face_image) for _ in range(3)]
        self.part = ["_head.png", "_eyes.png", "_chin.png"]
        self.jaw_range = list(range(1, 16))

    def write_image(self, indeces, ind):
        hull = cv2.convexHull(np.array(indeces))
        region_mask = np.zeros_like(self.gray)
        cv2.fillPoly(region_mask, [hull], 255)
        
        region = cv2.bitwise_and(self.face_image, self.face_image, mask=region_mask)
        self.output_image[ind] += region
        
        output_path = self.whole_image_path.split('.png')[0] + self.part[ind]
        cv2.imwrite(output_path, self.output_image[ind])
        
    def extract_regions(self):
        faces = self.hog_face_detector(self.gray)
        val = 80 # for our used sprite images always 80, but we may need to calcuate it.
        for face in faces:
            face_landmarks = self.dlib_facelandmark(self.gray, face)
            if face_landmarks.part(0).x < 256:
                val = face_landmarks.part(0).x

        # val is basically to ensure we don't overlap one image with another (i.e maintain 256 width for each image in sprite)
        for face in faces:
            face_landmarks = self.dlib_facelandmark(self.gray, face)

            pixel_st_x = face_landmarks.part(0).x - val
            pixel_end_x = pixel_st_x + 255

            # head
            self.write_image([[pixel_st_x, 0], [pixel_end_x, 0], [pixel_st_x, face_landmarks.part(19).y - 5],
                               [pixel_end_x, face_landmarks.part(19).y - 5]], 0)
            # eyes
            self.write_image([[pixel_st_x, face_landmarks.part(19).y - 6], [pixel_end_x, face_landmarks.part(19).y - 6],
                               [pixel_st_x, face_landmarks.part(28).y + 5], [pixel_end_x, face_landmarks.part(28).y + 5]], 1)

            indeces_ar = []
            change_in_curve = int(-0.1 * val)
            for i in range(len(self.jaw_range)):
                if self.jaw_range[i] == 9:
                    change_in_curve *= -1
                indeces_ar.append([face_landmarks.part(self.jaw_range[i]).x + change_in_curve,
                                   face_landmarks.part(self.jaw_range[i]).y])

            # chin
            indeces_ar.append([pixel_st_x + change_in_curve, face_landmarks.part(28).y + 4])
            indeces_ar.append([pixel_end_x - change_in_curve, face_landmarks.part(28).y + 4])
            self.write_image(indeces_ar, 2)

        # torso
        face_image = cv2.resize(self.face_image, (self.whole_image.shape[1], self.whole_image.shape[0]))
        face_gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

        _, mask = cv2.threshold(face_gray, 1, 255, cv2.THRESH_BINARY_INV)
        torso_image = cv2.bitwise_and(self.whole_image, self.whole_image, mask=mask)

        cv2.imwrite(self.whole_image_path.split('.png')[0] + '_torso.png', torso_image)
        
        change_background(self.whole_image_path.split('.png')[0] + '_torso.png')
        for i in self.part:
            change_background(self.whole_image_path.split('.png')[0] + i)