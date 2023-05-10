import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64

class Process:
    def tile_slide(input_image, path_to_model = "tflite_unet-epoch293.tflite"):
        if isinstance(input_image, str):
            img = cv2.imread(input_image)
        else: 
            #bytes --> nparray
            img = np.array(Image.open(io.BytesIO(input_image))) 
            #got rid of.read()

        img_shape = img.shape
        height = img_shape[0] #//2 rescale 
        width  = img_shape[1] # //2
        dim = (height,width)
        img = cv2.resize(img,dim)
        tile_size = (256, 256)
        offset = (256, 256)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("resize_tile.png",img)
        percentage_list =[]
        interpreter = tf.lite.Interpreter(model_path=path_to_model)
        interpreter.allocate_tensors()
        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        output_details = interpreter.get_output_details()
        block = []
        for i in range(0,img_shape[0],256):
            row_block = []
            for j in range(0,img_shape[1],256):
                cropped_img = img[i:i+256, j:j+256]
                im = np.asarray(cropped_img)
                height,width = im.shape
                if height == 256 and width == 256:
                    width = width//16*16
                    height = height//16*16
                    im = im[:height,:width]
                    if np.std(im) != 0 :
                        im = (im - np.mean(im))/np.std(im)
                    input_data = np.reshape(im, input_shape).astype(np.float32)
                    interpreter.set_tensor(input_details[0]['index'], input_data)
                    interpreter.invoke()
                    masks = interpreter.get_tensor(output_details[0]['index'])
                    non_zero = np.count_nonzero(masks)
                    masks_elements = masks.shape[0] * masks.shape[1]
                    zero = masks_elements - non_zero
                    percentage = (non_zero/masks_elements)*100
                    percentage_list.append(percentage)
                    row_block.append(masks)
                else:
                    masks = np.zeros((256,256))
                    row_block.append(masks)
            block.append(row_block)

        full_mask = np.block(block)
        save_mask = Image.fromarray(full_mask*255)
        save_mask = save_mask.convert("L")
        img_byte_arr = io.BytesIO()
        save_mask.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        average_tissue = (sum(percentage_list))/(len(percentage_list))
        return average_tissue*100, img_byte_arr