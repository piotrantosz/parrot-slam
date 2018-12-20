import cv2
from ar_markers import detect_markers

if __name__ == '__main__':
    print('Press "q" to quit')
    capture = cv2.VideoCapture('tcp://192.168.1.1:5555')

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
    sWH = 70

    # Expected drone movement
    # B - bottom
    # T - top
    # R - right
    # L - left
    # S - safe area / no movement
    #
    # | BR | B. | BL |
    # |--------------|
    # | R. | S. | L. |
    # |--------------|
    # | TR | T. | TL |


    # [(x1, y1), (x2, y2)]
    #
    # |<- x1,y1     |
    # |             |
    # |     x2,y2 ->|

    BR = [(0, 0), ((fW / 2) - (sWH / 2), (fH / 2) - (sWH / 2))]
    BL = [((fW / 2) + (sWH / 2), 0), (fW, (fH / 2) - (sWH / 2))]
    TR = [(0, fH), ((fW / 2) - (sWH / 2), (fH / 2) + (sWH / 2))]
    TL = [((fW / 2) + (sWH / 2), (fH / 2) + (sWH / 2)), (fW, fH)]

    while frame_captured:
        markers = detect_markers(frame)
        for marker in markers:
            print marker.center
            marker.highlite_marker(frame)

        overlay = frame.copy()
        opacity = 0.1

        # BR
        cv2.rectangle(overlay, BR[0], BR[1], (0, 255, 0), cv2.FILLED)

        # BL
        cv2.rectangle(overlay, BL[0], BL[1], (255, 0, 0), cv2.FILLED)
        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        # TR
        cv2.rectangle(overlay, TR[0], TR[1], (0, 0, 255), cv2.FILLED)
        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        # TL
        cv2.rectangle(overlay, TL[0], TL[1], (0, 255, 255), cv2.FILLED)
        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        cv2.imshow('Test Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_captured, frame = capture.read()

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
