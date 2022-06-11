import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

def runModel():
    #Load Model
    loaded = tf.saved_model.load("./")
    print(list(loaded.signatures.keys()))  # ["serving_default"]

    #Load signatures
    infer = loaded.signatures["serving_default"]
    print(infer.structured_input_signature)




ALPHA = 0.5
FONT = cv2.FONT_HERSHEY_PLAIN
TEXT_SCALE = 1.2
TEXT_THICKNESS = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_boxed_text(img, text, topleft, color):
    """Draw a transluent boxed text in white, overlayed on top of a
    colored patch surrounded by a black border. FONT, TEXT_SCALE,
    TEXT_THICKNESS and ALPHA values are constants (fixed) as defined
    on top.
    # Arguments
      img: the input image as a numpy array.
      text: the text to be drawn.
      topleft: XY coordinate of the topleft corner of the boxed text.
      color: color of the patch, i.e. background of the text.
    # Output
      img: note the original image is modified inplace.
    """
    assert img.dtype == np.uint8
    img_h, img_w, _ = img.shape
    if topleft[0] >= img_w or topleft[1] >= img_h:
        return img
    margin = 3
    size = cv2.getTextSize(text, FONT, TEXT_SCALE, TEXT_THICKNESS)
    w = size[0][0] + margin * 2
    h = size[0][1] + margin * 2
    # the patch is used to draw boxed text
    patch = np.zeros((h, w, 3), dtype=np.uint8)
    patch[...] = color
    cv2.putText(patch, text, (margin+1, h-margin-2), FONT, TEXT_SCALE,
                WHITE, thickness=TEXT_THICKNESS, lineType=cv2.LINE_8)
    cv2.rectangle(patch, (0, 0), (w-1, h-1), BLACK, thickness=1)
    w = min(w, img_w - topleft[0])  # clip overlay at image boundary
    h = min(h, img_h - topleft[1])
    # Overlay the boxed text onto region of interest (roi) in img
    roi = img[topleft[1]:topleft[1]+h, topleft[0]:topleft[0]+w, :]
    cv2.addWeighted(patch[0:h, 0:w, :], ALPHA, roi, 1 - ALPHA, 0, roi)
    return img

def rectangle_box(tags,img,cls,c1,c2,coor,prob,color):
  img=cv2.rectangle(img, c1, c2,color, 2)
  txt_loc = (max(int(coor[1]),0), max(int(coor[0])-15, 0))
  cls_name=tags[int(cls)]
  cf=float(prob)
  txt = '{} {:.2f}'.format(cls_name, cf)
  img = draw_boxed_text(img, txt, txt_loc, color)
  return img

def inference(img,tags,video = False):
    class_img=[]
    images_data=[]
    original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_data = cv2.resize(original_image, (416, 416))
    image_data = image_data / 255.
    images_data.append(image_data)
    batch_data = tf.constant(images_data)
    batch_data =tf.cast(batch_data, tf.float32)

    loaded = tf.saved_model.load("./")
    infer = loaded.signatures["serving_default"]
    
    pred_bbox =infer(batch_data)
    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]
        
    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                scores=tf.reshape(
                    pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                max_output_size_per_class=50,
                max_total_size=50,
                iou_threshold=0.3,
                score_threshold=0.5
            )

    for box,prob,cls in zip(boxes.numpy()[0],scores.numpy()[0],classes.numpy()[0]):
        if float(prob)>0.05:
          if not video:
            print(box)
            print(prob)
            print(cls)
          class_img.append(int(cls))
          coor=box
          image_h,image_w,_=img.shape

          coor[1] = coor[1] * image_w
          coor[0] = coor[0] * image_h

          coor[3] = coor[3] * image_w
          coor[2] = coor[2] * image_h

          c1, c2 = (coor[1].astype(int), coor[0].astype(int)), (coor[3].astype(int), coor[2].astype(int))
          print(c1)
          print(c2)
          img=rectangle_box(tags,img,cls,c1,c2,coor,prob,(255,0,0))
    
        if not video:
          print(classes)
          print(scores)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR),class_img