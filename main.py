import cv2

from detox_guard.face_detector import detect_face
from detox_guard.phone_detector import detect_phone
from detox_guard.ui_logger import draw_status, print_summary


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("웹캠을 실행할 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        face_detected = detect_face(frame)
        phone_detected = detect_phone(frame)

        if not face_detected or phone_detected:
            status = "경고"
        else:
            status = "집중 중"

        frame = draw_status(frame, status)

        cv2.imshow("Distraction Prevention", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()