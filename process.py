import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Process:
    def tile_slide(input_image, path_to_model = "tflite_unet-epoch293.tflite", file_path= ""):
        img = cv2.imread(input_image) # 512x512
        img_shape = img.shape
        height = img_shape[0] #//2 rescale 
        width  = img_shape[1] # //2
        dim = (height,width)
        #img = cv2.resize(img,dim)
        print(img.shape)
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
                    print(percentage)
                    if percentage > 1:
                        percentage_list.append(percentage)
                    row_block.append(masks)
                else:
                    print("This case")
                    masks = np.zeros((256,256))
                    row_block.append(masks)
                #cv2.imwrite(file_path + "/" + str(i//256) + "_" + str(j//256) + ".png", cropped_img)
            block.append(row_block)
            print(block)
        full_mask = np.block(block)
        save_mask = Image.fromarray(full_mask*255)
        save_mask = save_mask.convert("L")
        save_mask.save(input_image+"_mask.png")
        print("average globules percentage")
        average_tissue = (sum(percentage_list))/(len(percentage_list))
        plt.plot([i for i in range(len(percentage_list))],percentage_list)
        plt.savefig("steatosis_distribution_plot.png")
        print(average_tissue)
        return average_tissue, percentage_list, input_image+"_mask.png"