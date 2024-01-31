from image_processing import image_processor


def main() -> None:
    image_path = '../images/DSC_37501.jpg'
    
    image_processor_obj = image_processor(image_path)
    
    '''
    In images like sprite images if you want to process the whole image in parts
    then pass a small_image_dimensions array to this function which defines the 
    height and width of the small image chunks. 
    small_image_dimensions = [height, width] 
    ---> This project assumes that two consecutive faces have a gap of small_image_dimensions
    '''
    small_image_dimensions = [210, 256]
    image_processor_obj.process_image()

if __name__ == '__main__':
    main()