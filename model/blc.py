#!/usr/bin/python
import numpy as np
import sys

class BLC:
    'Black Level Compensation'

    def __init__(self, img, parameter, bayer_pattern, clip, mode):
        self.img = img
        self.parameter = parameter
        self.bayer_pattern = bayer_pattern
        self.clip = clip
        self.mode = mode

    def clipping(self, img):
        np.clip(img, 0, self.clip, out=img)
        return img

    def execute(self):
        raw_h = self.img.shape[0]
        raw_w = self.img.shape[1]
        blc_img = np.empty((raw_h,raw_w), np.int16)

        # r g r g r g
        # g b g b g b
        # r g r g r g
        # g b g b g b

        if self.mode == 'mean':
            blc_img = self.mean(blc_img)
        elif self.mode == 'alpha':
            blc_img = self.alpha(blc_img)

        print("min before BLC: ", np.min(self.img))
        print("max before BLC: ", np.max(self.img))
        print("min before clipping: ", np.min(blc_img))
        print("max before clipping: ", np.max(blc_img))
        blc_img = self.clipping(blc_img)
        print("min after clipping: ", np.min(blc_img))
        print("max after clipping: ", np.max(blc_img))

        return blc_img

    def mean(self, blc_img):
        bl_r = self.parameter[0]
        bl_gr = self.parameter[1]
        bl_gb = self.parameter[2]
        bl_b = self.parameter[3]
        alpha = self.parameter[4]
        beta = self.parameter[5]

        if self.bayer_pattern == 'rggb':
            r = self.img[::2, ::2]
            b = self.img[1::2, 1::2]
            gr = self.img[::2, 1::2]
            gb = self.img[1::2, ::2]
            print("max, min, mean of R", np.max(r), np.min(r), np.mean(r))
            print("max, min, mean of B", np.max(b), np.min(b), np.mean(b))
            print("max, min, mean of Gr", np.max(gr), np.min(gr), np.mean(gr))
            print("max, min, mean of Gb", np.max(gb), np.min(gb), np.mean(gb))

            r = r - np.mean(r)
            b = b - np.mean(b)
            gr = gr - np.mean(gr)
            gb = gb - np.mean(gb)

            blc_img[::2, ::2] = r
            blc_img[::2, 1::2] = gr
            blc_img[1::2, ::2] = gb
            blc_img[1::2, 1::2] = b
        elif self.bayer_pattern == 'bggr':
            b = self.img[::2, ::2]
            r = self.img[1::2, 1::2]
            gb = self.img[::2, 1::2]
            gr = self.img[1::2, ::2]
            blc_img[::2, ::2] = b
            blc_img[::2, 1::2] = gb
            blc_img[1::2, ::2] = gr
            blc_img[1::2, 1::2] = r
        elif self.bayer_pattern == 'gbrg':
            b = self.img[::2, 1::2] + bl_b
            r = self.img[1::2, ::2] + bl_r
            gb = self.img[::2, ::2] + bl_gb + beta * b / 256
            gr = self.img[1::2, 1::2] + bl_gr + alpha * r / 256
            blc_img[::2, ::2] = gb
            blc_img[::2, 1::2] = b
            blc_img[1::2, ::2] = r
            blc_img[1::2, 1::2] = gr
        elif self.bayer_pattern == 'grbg':
            r = self.img[::2, 1::2] + bl_r
            b = self.img[1::2, ::2] + bl_b
            gr = self.img[::2, ::2] + bl_gr + alpha * r / 256
            gb = self.img[1::2, 1::2] + bl_gb + beta * b / 256
            blc_img[::2, ::2] = gr
            blc_img[::2, 1::2] = r
            blc_img[1::2, ::2] = b
            blc_img[1::2, 1::2] = gb



        return blc_img


    def alpha(self, blc_img):
        bl_r = self.parameter[0]
        bl_gr = self.parameter[1]
        bl_gb = self.parameter[2]
        bl_b = self.parameter[3]
        alpha = self.parameter[4]
        beta = self.parameter[5]


        if self.bayer_pattern == 'rggb':
            r = self.img[::2, ::2] + bl_r
            # for j in range(len(r)):
            #     for i in range(len(r[0])):
                    # print(j,i)
                    # print(r[j][i])
            print("R row", len(r))
            print("R col", len(r[0]))
            b = self.img[1::2, 1::2] + bl_b
            print("B row", len(b))
            print("B col", len(b[0]))
            gr = self.img[::2, 1::2] + bl_gr + alpha * r / 256
            print("Gr row", len(gr))
            print("Gr col", len(gr[0]))
            gb = self.img[1::2, ::2] + bl_gb + beta * b / 256
            print("Gb row", len(gb))
            print("Gb col", len(gb[0]))
            blc_img[::2, ::2] = r
            blc_img[::2, 1::2] = gr
            blc_img[1::2, ::2] = gb
            blc_img[1::2, 1::2] = b
        elif self.bayer_pattern == 'bggr':
            b = self.img[::2, ::2] + bl_b
            r = self.img[1::2, 1::2] + bl_r
            gb = self.img[::2, 1::2] + bl_gb + beta * b / 256
            gr = self.img[1::2, ::2] + bl_gr + alpha * r / 256
            blc_img[::2, ::2] = b
            blc_img[::2, 1::2] = gb
            blc_img[1::2, ::2] = gr
            blc_img[1::2, 1::2] = r
        elif self.bayer_pattern == 'gbrg':
            b = self.img[::2, 1::2] + bl_b
            r = self.img[1::2, ::2] + bl_r
            gb = self.img[::2, ::2] + bl_gb + beta * b / 256
            gr = self.img[1::2, 1::2] + bl_gr + alpha * r / 256
            blc_img[::2, ::2] = gb
            blc_img[::2, 1::2] = b
            blc_img[1::2, ::2] = r
            blc_img[1::2, 1::2] = gr
        elif self.bayer_pattern == 'grbg':
            r = self.img[::2, 1::2] + bl_r
            b = self.img[1::2, ::2] + bl_b
            gr = self.img[::2, ::2] + bl_gr + alpha * r / 256
            gb = self.img[1::2, 1::2] + bl_gb + beta * b / 256
            blc_img[::2, ::2] = gr
            blc_img[::2, 1::2] = r
            blc_img[1::2, ::2] = b
            blc_img[1::2, 1::2] = gb

        return blc_img

