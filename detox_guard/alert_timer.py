import time
import platform

# 윈도우 환경에서만 비프음 모듈 로드 (맥/리눅스 실행 시 오류 방지)
if platform.system() == "Windows":
    import winsound


class AlertTimer:
    def __init__(self, cooldown_sec=3.0):
        self.total_focus_sec = 0.0           # 누적 집중 시간(초)
        self.last_check_time = time.time()   # 직전 프레임 체크 시간
        self.warning_count = 0               # 총 경고 횟수
        self.last_alert_time = 0.0           # 마지막 경고 발생 시간
        self.cooldown_sec = cooldown_sec     # 경고 연속 울림 방지 간격(초)

    def update(self, is_distracted: bool) -> bool:
        """
        매 프레임마다 호출되는 상태 업데이트 메서드
        - is_distracted가 True면(자리 비움 또는 스마트폰 감지): 경고 발생 후 True 반환
        - is_distracted가 False면(정상 집중): 집중 시간 누적 후 False 반환
        """
        now = time.time()
        elapsed = now - self.last_check_time
        self.last_check_time = now

        if is_distracted:
            if now - self.last_alert_time >= self.cooldown_sec:
                self.warning_count += 1
                self.last_alert_time = now
                self._play_beep()
                print(f"[경고 {self.warning_count}회] 집중이 흐트러졌습니다! 자리에 앉아 스마트폰을 치워주세요.")
            return True
        else:
            self.total_focus_sec += elapsed
            return False

    def _play_beep(self):
        """경고음 출력"""
        if platform.system() == "Windows":
            winsound.Beep(1000, 300)  # 1000Hz, 0.3초 비프음
        else:
            print("\a", end="")

    def get_formatted_focus_time(self) -> str:
        """누적 집중 시간을 'MM:SS' 형식 문자열로 반환"""
        minutes = int(self.total_focus_sec // 60)
        seconds = int(self.total_focus_sec % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def get_summary(self) -> dict:
        """프로그램 종료 시 요약 데이터 반환"""
        return {
            "focus_time": self.get_formatted_focus_time(),
            "warning_count": self.warning_count
        }


# 단독 실행 테스트용 (통합 실행 시에는 동작하지 않음)
if __name__ == "__main__":
    print("=== AlertTimer 단독 테스트 시작 ===")
    timer = AlertTimer(cooldown_sec=2.0)

    print("1. 정상 집중 상태 3초 테스트...")
    for _ in range(3):
        timer.update(is_distracted=False)
        time.sleep(1)
    print("누적 집중 시간:", timer.get_formatted_focus_time())

    print("2. 딴짓 감지(True) 경고 테스트...")
    timer.update(is_distracted=True)
    time.sleep(1)

    print("종료 요약 데이터:", timer.get_summary())