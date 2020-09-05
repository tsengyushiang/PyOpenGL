import cv2
import numpy as np


class Aruco():
    def __init__(self):
        # Load the dictionary that was used to generate the markers.
        self.dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

        # Initialize the detector parameters using default values
        self.parameters = cv2.aruco.DetectorParameters_create()

    def saveMarkers(self):
        # Load the predefined dictionary
        dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

        # Generate the marker
        markerImage1 = np.zeros((200, 200), dtype=np.uint8)
        markerImage2 = np.zeros((200, 200), dtype=np.uint8)
        markerImage3 = np.zeros((200, 200), dtype=np.uint8)

        markerImage33 = cv2.aruco.drawMarker(
            dictionary, 33, 200, markerImage1, 1)
        markerImage34 = cv2.aruco.drawMarker(
            dictionary, 34, 200, markerImage2, 1)
        markerImage35 = cv2.aruco.drawMarker(
            dictionary, 35, 200, markerImage3, 1)

        cv2.imwrite("marker33.png", markerImage33)
        cv2.imwrite("marker34.png", markerImage34)
        cv2.imwrite("marker35.png", markerImage35)

    def findMarkers(self, color_image):
        # Detect the markers in the image
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(
            color_image, self.dictionary, parameters=self.parameters)

        for markerCorner in markerCorners:
            cv2.circle(
                color_image, (markerCorner[0][0][0], markerCorner[0][0][1]), 15, (0, 255, 255), 3)
            cv2.circle(
                color_image, (markerCorner[0][1][0], markerCorner[0][1][1]), 15, (0, 0, 255), 3)
            cv2.circle(
                color_image, (markerCorner[0][2][0], markerCorner[0][2][1]), 15, (255, 0, 255), 3)
            cv2.circle(
                color_image, (markerCorner[0][3][0], markerCorner[0][3][1]), 15, (255, 255,), 3)
