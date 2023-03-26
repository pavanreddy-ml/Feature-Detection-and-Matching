import cv2
import numpy as np

class AR():
    def __init__(self):
        pass

    def get_features(self, image, params, algorithm='harris', ):
        img = image.copy()

        if algorithm == 'None':
            return [img]
        elif algorithm == 'harris':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_image = np.float32(gray_image)
            dst = cv2.cornerHarris(gray_image, blockSize=params["Block Size"], ksize=(params["Kernel Size"]*2)+1, k=params["K"])
            dst = cv2.dilate(dst, None)
            img[dst > 0.01 * dst.max()] = [0, 0, 255]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, dst
        elif algorithm == 'shitomasi':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_image = np.float32(gray_image)
            corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=params["Features"], qualityLevel=params["Quality Control"], minDistance=params["Min Distance"])
            corners = np.float32(corners)
            for item in corners:
                x, y = item[0]
                x = int(x)
                y = int(y)
                cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, corners
        elif algorithm == 'sift':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sift = cv2.xfeatures2d.SIFT_create(nfeatures=params["Features"], contrastThreshold=params["Contrast Threshold"], nOctaveLayers=params["Octave Layers"])
            kp, des = sift.detectAndCompute(gray_image, None)
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, kp, des
        elif algorithm == 'fast':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fast = cv2.FastFeatureDetector_create(threshold=params["Threshold"], nonmaxSuppression=params["Non Max Suppression"])
            kp = fast.detect(gray_image, 0)
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, kp
        elif algorithm == 'orb':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            orb = cv2.ORB_create(nfeatures=params["Features"], scaleFactor=params["Scale Factor"], nlevels=params["Levels"], edgeThreshold=params["Edge Threshold"])
            kp, des = orb.detectAndCompute(gray_image, None)
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255), flags=0)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, kp, des



    def match_features(self, source_image, dest_image, params, det_algorithm='orb'):
        _, kp1, des1 = self.get_features(source_image, algorithm=det_algorithm, params=params)
        _, kp2, des2 = self.get_features(dest_image, algorithm=det_algorithm, params=params)

        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        no_of_matches = brute_force.match(des1, des2)

        no_of_matches = sorted(no_of_matches, key=lambda x: x.distance)

        output_image = cv2.drawMatches(source_image, kp1, dest_image, kp2, no_of_matches[:params['Features']], None, flags=2)

        output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

        return output_image


__name__ = "__main__"

image = cv2.imread('MarkerIcons01.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = np.float32(gray_image)

image2 = cv2.imread('m1.jpg')
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
gray_image2 = np.float32(gray_image2)

# ar = AR()
# operation = 'detection'
# if operation == 'detection':
#     disp = ar.get_features(image, algorithm='harris')[0]
# elif operation == 'matching':
#     disp = ar.match_features(image, image2, det_algorithm='orb')
#
# cv2.imshow('haris_corner', disp)
# cv2.waitKey()