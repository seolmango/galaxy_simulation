# galaxy_simulation
두 은하의 충돌을 python으로 시뮬레이션하고 matplotlib로 시각화하는 코드입니다.

![예시](example.jpg)

## How to Use

```bash
python main.py
```

입력 이후 설정값들을 입력합니다. 이후 실시간 시각화와 함께 시뮬레이션이 시작됩니다.
이후에 다시 시각화가 필요하시다면 main.py를 실행하면 생성되는 simulation.npy 파일을 make_video.py를 이용하여 시각화하여 mp4로 저장할 수 있습니다.

```bash
python make_video.py simulation.npy
```

## 참고 자료

Verkade, T. (2020). Simulating Galaxy Collisions in Python for Astronomy Education (Doctoral dissertation).