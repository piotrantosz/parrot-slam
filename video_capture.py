import cv2
from ar_markers import detect_markers

if __name__ == '__main__':
    print('Press "q" to quit')
    # capture = cv2.VideoCapture('tcp://192.168.1.1:5555')
    capture = cv2.VideoCapture(0)

    if capture.isOpened():
        frame_captured, frame = capture.read()
    else:
        frame_captured = False

    # Frame size
    fW = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # 640
    fH = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 360
    # Frame center point
    fC = ((fW / 2), (fH / 2))
    # Safe area width/height
    sWH = 80

    # Expected drone movement depending on marker position
    # B - bottom
    # T - top
    # R - right
    # L - left
    # S - safe area / no movement
    #

    # | TL | T. | TR |
    # |--------------|
    # | L. | S. | R. |
    # |--------------|
    # | BL | B. | BR |


    # [(x1, y1), (x2, y2)]
    # structure : [(,),(,)]
    #
    # |<- x1,y1     |
    # |             |
    # |     x2,y2 ->|

    TL = [(0, 0), ((fW / 2) - (sWH / 2), (fH / 2) - (sWH / 2))]
    TR = [((fW / 2) + (sWH / 2), 0), (fW, (fH / 2) - (sWH / 2))]
    BL = [(0, fH/2 + sWH / 2), ((fW / 2) - (sWH / 2), fH)]
    BR = [((fW / 2) + (sWH / 2), (fH / 2) + (sWH / 2)), (fW, fH)]
    T = [((fW / 2 - sWH / 2), 0), ((fW / 2 + sWH / 2), (fH / 2 - sWH / 2))]
    B = [((fW / 2 - sWH / 2), (fH / 2 + sWH / 2)), ((fW / 2 + sWH / 2), fW)]
    R = [((fW / 2 + sWH / 2), (fH / 2 - sWH / 2)), (fW, (fH / 2 + sWH / 2))]
    L = [(0, (fH / 2 - sWH / 2)), ((fW / 2 - sWH / 2), (fH / 2 + sWH / 2))]
    S = [((fW / 2) - (sWH / 2), (fH / 2) - (sWH / 2)), (((fW / 2) - (sWH / 2) + sWH), ((fH / 2) - (sWH / 2)) + sWH)]

    while frame_captured:
        markers = detect_markers(frame)
        for marker in markers:
            x = marker.center[0]
            y = marker.center[1]
            txt = ''

            if (x > BR[0][0] and x < BR[1][0] and y > BR[0][1] and y < BR[1][1]):
                txt = "move BOTTOM RIGHT"
            elif (x > BL[0][0] and x < BL[1][0] and y > BL[0][1] and y < BL[1][1]):
                txt = "move BOTTOM LEFT"
            elif (x > TR[0][0] and x < TR[1][0] and y > TR[0][1] and y < TR[1][1]):
                txt = "move TOP RIGHT"
            elif (x > TL[0][0] and x < TL[1][0] and y > TL[0][1] and y < TL[1][1]):
                txt = "move TOP LEFT"
            elif (x > B[0][0] and x < B[1][0] and y > B[0][1] and y < B[1][1]):
                txt = "move BOTTOM"
            elif (x > T[0][0] and x < T[1][0] and y > T[0][1] and y < T[1][1]):
                txt = "move TOP"
            elif (x > L[0][0] and x < L[1][0] and y > L[0][1] and y < L[1][1]):
                txt = "move LEFT"
            elif (x > R[0][0] and x < R[1][0] and y > R[0][1] and y < R[1][1]):
                txt = "move RIGHT"
            elif (x > S[0][0] and x < S[1][0] and y > S[0][1] and y < S[1][1]):
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

            marker.highlite_marker(frame)

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
            break
        frame_captured, frame = capture.read()

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
