import cv2
import numpy as np

def addLasers(frame, x, y, frame_w, frame_h, eye_x, eye_y, eye_width, eye_height, lens):

    # preparo lasers
    lens_h_og, lens_w_og, lens_ch = lens.shape;
    lens_h = int(1.7*eye_height);
    lens_w = lens_h;


    #coordenadas del laser/lens
    #eye_x and eye_y son relativos a x e y
    lens_x1 = eye_x + x - int(eye_width//4);
    lens_x2 = lens_x1 + lens_w;
    lens_y1 = y + eye_y - int(eye_height//4);
    lens_y2 = lens_y1 + lens_h;


    #
    #
    #reviso que no se vaya del img.w e img.h
    if lens_x1 < 0: lens_x1 = 0;
    if lens_y1 < 0: lens_y1 = 0;
    if lens_x2 > frame_w: lens_x2 = frame_w;
    if lens_y2 > frame_h: lens_y2 = frame_h;
    #


    #resizeo lens para que entre en el area del ojo
    lens = cv2.resize(lens, (lens_w, lens_h), interpolation = cv2.INTER_AREA);

    ret, og_mask = cv2.threshold(cv2.cvtColor(lens, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY_INV);
    og_mask_inv = cv2.bitwise_not(og_mask);

    mask = cv2.resize(og_mask, (lens_w, lens_h), interpolation = cv2.INTER_AREA);
    mask_inv = cv2.resize(og_mask_inv, (lens_w, lens_h), interpolation = cv2.INTER_AREA);

    roi = frame[lens_y1:lens_y2, lens_x1:lens_x2];

    roi_bg = cv2.bitwise_and(roi, roi, mask=mask);
    roi_fg = cv2.bitwise_and(lens, lens, mask=mask_inv);

    roi_fg = roi_fg[:,:,0:3];
    dst = cv2.add(roi_bg, roi_fg);

    # put back in original image
    frame[lens_y1:lens_y2, lens_x1:lens_x2] = dst;


    return frame;