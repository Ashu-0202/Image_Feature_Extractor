from image_processing import image_processor


def main() -> None:
    image_path = '../images/male_en-gb.png'
    
    image_processor_obj = image_processor(image_path)
    
    '''
    In images like sprite images if you want to process the whole image in parts
    then pass an small_image_dimensions array to this function which defines the 
    height and width in which you want to process the whole image 
    small_image_dimensions = [height, width]
    
    otherwise it will process the whole image as at once 
    (this only works with one face in the image)
    '''
    small_image_dimensions = [210, 256]
    image_processor_obj.process_image(small_image_dimensions)

if __name__ == '__main__':
    main()