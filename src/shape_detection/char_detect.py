# -*- coding: utf-8 -*-
__author__ = 'hironand'

import cv2

'''

文字の特徴量を抽出し、形状マッチングをしてみる
比較：フォント文字と習字文字
使用する文字は、永字八法の「永」の字

'''
def main():

    # マスター：「永」のゴシック体と明朝体
    ei_gothic = cv2.imread("./../../image/ei_gothic.png")
    ei_mincho = cv2.imread("./../../image/ei_mincho.png")

    # サンプル：習字で書かれた文字
    ei001 = cv2.imread("./../../image/ei001.png")
    ei002 = cv2.imread("./../../image/ei002.png")

    # 特徴量抽出
    kp_m, des_m = detect(ei_gothic, "ei_gothic.png")
    kp_s, des_s = detect(ei001, "ei001.png")

    # マッチング
    master = "ei_gothic", ei_gothic, kp_m, des_m
    sample = "ei001", ei001, kp_s, des_s
    match_FLANN(master, sample)


# 特徴量(KeyPoint, Descriptor)抽出
def detect(img, name):

    detector = cv2.AKAZE_create()
    kp, des = detector.detectAndCompute(img, None)
    print("{}: keypoints: {}, descriptors: {}".format(name, len(kp), des.shape))

    cv2.drawKeypoints(img, kp, img, (0, 255, 0))
    cv2.imwrite("./../../image/detect_" + name, img)

    return kp, des

# FLANN based Matcher で特徴量を比較
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

    match_img = cv2.drawMatchesKnn(img_m, kp_m, img_s, kp_s, matches, None, **draw_params)
    cv2.imwrite("./../../image/match_{}_{}".format(name_m, name_s), match_img)


main()
