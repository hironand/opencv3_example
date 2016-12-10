# -*- coding: utf-8 -*-
__author__ = 'hironand'

import cv2
import numpy as np

'''

文字の特徴量を抽出し、形状マッチングをしてみる
比較：フォント文字と習字文字
使用する文字は、永字八法の「永」の字

'''
def main():

    # マスター：「永」のゴシック体と明朝体
    ei_gothic = "gothic", cv2.imread("./../../image/ei_gothic.png")
    ei_mincho = "mincho", cv2.imread("./../../image/ei_mincho.png")
    ei_master = [ei_gothic, ei_mincho]

    # サンプル：習字で書かれた文字
    ei001 = "ei001", cv2.imread("./../../image/ei001.png")
    ei002 = "ei002", cv2.imread("./../../image/ei002.png")
    ei_sample = [ei001, ei002]


    for master_name, master_img in ei_master:
        for sample_name, sample_img in ei_sample:

            # 特徴量抽出
            kp_m, des_m = detect_AKAZE(master_img, master_name)
            kp_s, des_s = detect_AKAZE(sample_img, sample_name)

            # マッチング
            master = master_name, master_img, kp_m, des_m
            sample = sample_name, sample_img, kp_s, des_s
            match_BF(master, sample)



# AKAZEで特徴量(KeyPoint, Descriptor)抽出
def detect_AKAZE(img, name):

    detector = cv2.AKAZE_create()
    kp, des = detector.detectAndCompute(img, None)
    print("{}: keypoints: {}, descriptors: {}".format(name, len(kp), des.shape))

    cv2.drawKeypoints(img, kp, img, (0, 255, 0))
    cv2.imwrite("./../../image/AKAZE_{}.png".format(name), img)

    return kp, des


# BF(Brute-Force) で特徴量を比較
# * FLANNはPython2.7 では動作しなかった
def match_BF((name_m, img_m, kp_m, des_m), (name_s, img_s, kp_s, des_s)):

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des_m, des_s)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    # Draw first 10 matches.
    out_img = cv2.drawMatches(img_m, kp_m, img_s, kp_s, matches ,None, flags=2)
    out_name = "./../../image/BF_{}_{}.png".format(name_m, name_s)
    cv2.imwrite(out_name, out_img)


# BF(Brute-Force) で特徴量を比較
# * FLANNはPython2.7 では動作しなかった
def match_BF_((name_m, img_m, kp_m, des_m), (name_s, img_s, kp_s, des_s)):

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des_m, des_s, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in xrange(len(matches))]
    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)

    # cv2.drawMatchesKnn expects list of lists as matches.
    out_img = cv2.drawMatchesKnn(img_m, kp_m, img_s, kp_s, good, outImg=np.zeros)
    cv2.imwrite("./../../image/BF_{}_{}".format(name_m, name_s), out_img)



# FLANN で特徴量を比較
def match_FLANN((name_m, img_m, kp_m, des_m), (name_s, img_s, kp_s, des_s)):
    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des_m, des_s, k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in xrange(len(matches))]

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)

    out_img = cv2.drawMatchesKnn(img_m, kp_m, img_s, kp_s, matches, None, **draw_params)
    cv2.imwrite("./../../image/FLANN_{}_{}".format(name_m, name_s), out_img)


main()
