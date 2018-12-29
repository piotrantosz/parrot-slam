import cv2
import sys
import api.libardrone as libardrone
import time

if __name__ == '__main__':
    print('Press "q" to quit')

    cascPath = sys.argv[1]
    faceCascade = cv2.CascadeClassifier(cascPath)
    capture = cv2.VideoCapture('tcp://192.168.1.1:5555')
    # capture = cv2.VideoCapture(0)

    drone = libardrone.ARDrone()
    drone.trim()
    drone.takeoff()

    if capture.isOpened():
        frame_captured, frame = capture.read()
    else:
        frame_captured = False

    # Frame size
    fW = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # ar 2.0 : 640
    fH = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # ar 2.0 : 360
    # Frame center point
    fC = ((fW / 2), (fH / 2))
    # Safe area width/height
    sWH = 90

    # Expected drone movement depending on marker position
    # B - bottom
    # T - top
    # R - right
    # L - left
    # S - safe area / no movement

    # | TL | T. | TR |
    # |--------------|
    # | L. | S. | R. |  2D VIEW
    # |--------------|
    # | BL | B. | BR |

    # [(x1, y1), (x2, y2)]
    # structure : [(,),(,)]
    #
    # |<- x1,y1     |
    # |             |
    # |     x2,y2 ->|

    # TODO
    # test w. connection to drone
    # add other axis (front, right left with stable axis Y)

    TL = [(0, 0), ((fW / 2) - (sWH / 2), (fH / 2) - (sWH / 2))]
    TR = [((fW / 2) + (sWH / 2), 0), (fW, (fH / 2) - (sWH / 2))]
    BL = [(0, fH / 2 + sWH / 2), ((fW / 2) - (sWH / 2), fH)]
    BR = [((fW / 2) + (sWH / 2), (fH / 2) + (sWH / 2)), (fW, fH)]
    T = [((fW / 2 - sWH / 2), 0), ((fW / 2 + sWH / 2), (fH / 2 - sWH / 2))]
    B = [((fW / 2 - sWH / 2), (fH / 2 + sWH / 2)), ((fW / 2 + sWH / 2), fW)]
    R = [((fW / 2 + sWH / 2), (fH / 2 - sWH / 2)), (fW, (fH / 2 + sWH / 2))]
    L = [(0, (fH / 2 - sWH / 2)), ((fW / 2 - sWH / 2), (fH / 2 + sWH / 2))]
    S = [((fW / 2) - (sWH / 2), (fH / 2) - (sWH / 2)), (((fW / 2) - (sWH / 2) + sWH), ((fH / 2) - (sWH / 2)) + sWH)]

    while frame_captured:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            faceCenter = ((x + w / 2), (y + h / 2))
            faceCenterX = faceCenter[0]
            faceCenterY = faceCenter[1]

            # Draw a rectangle around the faces
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            txt = ''

            if (faceCenter[0] > TL[0][0] and faceCenter[0] < TL[1][0] and faceCenter[1] > TL[0][1] and faceCenter[1] < TL[1][1]):
                drone.move_left()
                drone.move_up()
                txt = "move TOP LEFT"
            elif (faceCenter[0] > TR[0][0] and faceCenter[0] < TR[1][0] and faceCenter[1] > TR[0][1] and faceCenter[1] < TR[1][1]):
                drone.move_right()
                drone.move_up()
                txt = "move TOP RIGHT"
            elif (faceCenter[0] > BL[0][0] and faceCenter[0] < BL[1][0] and faceCenter[1] > BL[0][1] and faceCenter[1] < BL[1][1]):
                drone.move_left()
                drone.move_down()
                txt = "move BOTTOM LEFT"
            elif (faceCenter[0] > BR[0][0] and faceCenter[0] < BR[1][0] and faceCenter[1] > BR[0][1] and faceCenter[1] < BR[1][1]):
                drone.move_right()
                drone.move_down()
                txt = "move BOTTOM RIGHT"
            elif (faceCenter[0] > T[0][0] and faceCenter[0] < T[1][0] and faceCenter[1] > T[0][1] and faceCenter[1] < T[1][1]):
                drone.move_up()
                txt = "move TOP"
            elif (faceCenter[0] > B[0][0] and faceCenter[0] < B[1][0] and faceCenter[1] > B[0][1] and faceCenter[1] < B[1][1]):
                drone.move_down()
                txt = "move BOTTOM"
            elif (faceCenter[0] > R[0][0] and faceCenter[0] < R[1][0] and faceCenter[1] > R[0][1] and faceCenter[1] < R[1][1]):
                drone.move_right()
                txt = "move RIGHT"
            elif (faceCenter[0] > L[0][0] and faceCenter[0] < L[1][0] and faceCenter[1] > L[0][1] and faceCenter[1] < L[1][1]):
                drone.move_left()
                txt = "move LEFT"
            elif (faceCenter[0] > S[0][0] and faceCenter[0] < S[1][0] and faceCenter[1] > S[0][1] and y < S[1][1]):
                txt = "OK"

            font = cv2.FONT_HERSHEY_SIMPLEX
            textPosition = (10, 50)
            fontScale = 0.8
            fontColor = (255, 255, 255)
            lineType = 2

            cv2.putText(frame, txt,
                        textPosition,
                        font,
                        fontScale,
                        fontColor,
                        lineType)

        overlay = frame.copy()
        opacity = 0.1

        # TL
        cv2.rectangle(overlay, TL[0], TL[1], (0, 0, 255), cv2.FILLED)
        # TR
        cv2.rectangle(overlay, TR[0], TR[1], (0, 0, 255), cv2.FILLED)
        # BL
        cv2.rectangle(overlay, BL[0], BL[1], (0, 0, 255), cv2.FILLED)
        # BR
        cv2.rectangle(overlay, BR[0], BR[1], (0, 0, 255), cv2.FILLED)
        # T
        cv2.rectangle(overlay, T[0], T[1], (0, 255, 255), cv2.FILLED)
        # B
        cv2.rectangle(overlay, B[0], B[1], (0, 255, 255), cv2.FILLED)
        # R
        cv2.rectangle(overlay, R[0], R[1], (0, 255, 255), cv2.FILLED)
        # L
        cv2.rectangle(overlay, L[0], L[1], (0, 255, 255), cv2.FILLED)
        # S
        cv2.rectangle(overlay, S[0], S[1], (0, 255, 0), cv2.FILLED)

        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        cv2.imshow('Test Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break
        frame_captured, frame = capture.read()

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
