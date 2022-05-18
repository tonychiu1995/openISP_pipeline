#!/usr/bin/python
import numpy as np

class DPC:
    'Dead Pixel Correction'

    def __init__(self, img, thres, mode, clip):
        self.img = img
        self.thres = thres
        self.mode = mode
        self.clip = clip

    def padding(self):
        img_pad = np.pad(self.img, (2, 2), 'reflect')
        return img_pad

    def clipping(self, img):
        np.clip(img, 0, self.clip, out=img)
        return img

    def execute(self):
        img_pad = self.padding()
        raw_h = self.img.shape[0]
        raw_w = self.img.shape[1]
        dpc_img = np.empty((raw_h, raw_w), np.uint16)

        count = 0
        for y in range(raw_h - 4):
            for x in range(raw_w - 4):
                # p1 p2 p3
                # p4 p0 p5
                # p6 p7 p8

                p0 = int(img_pad[y + 2][x + 2])
                p1 = int(img_pad[y][x])
                p2 = int(img_pad[y][x + 2])
                p3 = int(img_pad[y][x + 4])
                p4 = int(img_pad[y + 2][x])
                p5 = int(img_pad[y + 2, x + 4])
                p6 = int(img_pad[y + 4, x])
                p7 = int(img_pad[y + 4, x + 2])
                p8 = int(img_pad[y + 4, x + 4])

                # detect p0 by the threshold if the pixel level is always larger than the threshold, we need dpc

                for px in [p1, p2, p3, p4, p5, p6, p7]:
                    if abs(px - p0) <= self.thres:
                        dpc = False
                        break
                    else:
                        dpc = True
                    # print(abs(px - p0), px, p0, int(px)-int(p0))
                # print(self.thres)

                # if (abs(p1 - p0) > self.thres) and (abs(p2 - p0) > self.thres) and (abs(p3 - p0) > self.thres) \
                #         and (abs(p4 - p0) > self.thres) and (abs(p5 - p0) > self.thres) and (abs(p6 - p0) > self.thres) \
                #         and (abs(p7 - p0) > self.thres) and (abs(p8 - p0) > self.thres):
                if dpc is True:
                    count += 1
                    print("[" + self.mode + "] Execute dead pixel correlation for ({y},{x}), count = {c}...".format(x=x, y=y, c=count))
                    print("before correction: ",p0)
                    if self.mode == 'mean':
                        p0 = (p2 + p4 + p5 + p7) / 4
                    elif self.mode == 'gradient':
                        dv = abs(2 * p0 - p2 - p7)
                        dh = abs(2 * p0 - p4 - p5)
                        ddl = abs(2 * p0 - p1 - p8)
                        ddr = abs(2 * p0 - p3 - p6)
                        if (min(dv, dh, ddl, ddr) == dv):
                            p0 = (p2 + p7 + 1) / 2
                            print("p0, dv", p0, dv)
                        elif (min(dv, dh, ddl, ddr) == dh):
                            p0 = (p4 + p5 + 1) / 2
                            print("p0, dh", p0, dh)
                        elif (min(dv, dh, ddl, ddr) == ddl):
                            p0 = (p1 + p8 + 1) / 2
                            print("p0, ddl", p0, ddl)
                        else:
                            p0 = (p3 + p6 + 1) / 2
                            print("p0, ddr", p0, ddr)
                dpc_img[y, x] = p0
        dpc_img = np.uint16(dpc_img)
        dpc_img = self.clipping(dpc_img)

        # self.img = dpc_img
        return dpc_img

