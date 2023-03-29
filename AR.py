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
            dst = cv2.cornerHarris(gray_image, blockSize=params["Block Size"], ksize=(params["Kernel Size"] * 2) + 1,
                                   k=params["K"])
            dst = cv2.dilate(dst, None)
            img[dst > 0.01 * dst.max()] = [0, 0, 255]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, dst
        elif algorithm == 'shitomasi':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_image = np.float32(gray_image)
            corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=params["Features"],
                                              qualityLevel=params["Quality Control"],
                                              minDistance=params["Min Distance"])
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
            sift = cv2.xfeatures2d.SIFT_create(nfeatures=params["Features"],
                                               contrastThreshold=params["Contrast Threshold"],
                                               nOctaveLayers=params["Octave Layers"])
            kp, des = sift.detectAndCompute(gray_image, None)
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, kp, des
        elif algorithm == 'fast':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fast = cv2.FastFeatureDetector_create(threshold=params["Threshold"],
                                                  nonmaxSuppression=params["Non Max Suppression"])
            kp = fast.detect(gray_image, 0)
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, kp
        elif algorithm == 'orb':
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            orb = cv2.ORB_create(nfeatures=params["Features"], scaleFactor=params["Scale Factor"],
                                 nlevels=params["Levels"], edgeThreshold=params["Edge Threshold"])
            kp, des = orb.detectAndCompute(gray_image, None)
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255), flags=0)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, kp, des

    def match_features(self, marker, frame, aug_image, params, det_algorithm='orb'):
        try:

            marker = cv2.cvtColor(marker, cv2.COLOR_BGR2RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            aug_image = cv2.cvtColor(aug_image, cv2.COLOR_BGR2RGB)

            # Matching
            _, kp1, des1 = self.get_features(marker, algorithm=det_algorithm, params=params)
            _, kp2, des2 = self.get_features(frame, algorithm=det_algorithm, params=params)

            brute_force = cv2.BFMatcher()
            matches = brute_force.knnMatch(des1, des2, k=2)

            good = []
            for m, n in matches:
                if m.distance < 0.9 * n.distance:
                    good.append(m)

            srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)

            pts = np.float32(
                [[0, 0], [0, marker.shape[1]], [marker.shape[1], marker.shape[0]], [marker.shape[0], 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, matrix)
            x = frame.copy()
            mat_21 = cv2.polylines(x, [np.int32(dst)], True, (0, 0, 255), 3)

            maskNew = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
            maskInv = cv2.bitwise_not(maskNew)

            mat_22 = cv2.bitwise_and(frame, frame, mask=maskNew)
            aug_21 = cv2.bitwise_and(frame, frame, mask=maskInv)

            aug_12 = cv2.warpPerspective(aug_image, matrix, (frame.shape[1], frame.shape[0]),
                                         borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 255, 0))
            aug_12_black = cv2.warpPerspective(aug_image, matrix, (frame.shape[1], frame.shape[0]),
                                         borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

            aug_22 = cv2.bitwise_or(aug_21, aug_12_black)

            output_image1 = cv2.drawMatches(marker, kp1, frame, kp2, good, None, flags=2)
            output_image2 = cv2.hconcat([mat_21, mat_22])
            matching_output = cv2.vconcat([output_image1, output_image2])

            output_image3 = cv2.hconcat([aug_image, aug_12])
            output_image4 = cv2.hconcat([aug_21, aug_22])
            augmentation_output = cv2.vconcat([output_image3, output_image4])

            return matching_output, augmentation_output
        except:
            output_image1 = cv2.hconcat([marker, frame])
            output_image2 = cv2.hconcat([frame, frame])
            matching_output = cv2.vconcat([output_image1, output_image2])

            output_image3 = cv2.hconcat([aug_image, aug_image])
            output_image4 = cv2.hconcat([frame, frame])
            augmentation_output = cv2.vconcat([output_image3, output_image4])

            return matching_output, augmentation_output


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
