### Synopsis

*python file* [*FILE PATH*] [*BOARD ID*]

### Description

PCB 검사 시뮬레이션 실행 할 경우 옵션들에 대한 설명

### Input

- *FILE PATH* : 검사할 이미지 데이터 경로 입력 (ex. C:\PCB_inspection\comp_images)
- *BOARD ID* : 검사할 보드의 종류/명칭 (ex. HC-06)

####   Input Example

```
./inspection.py C:\PCB_inspection\comp_images HC-06
```
- 파일 상세 경로는 다음과 같음

  학습) [*BOARD ID*] \ [*LEARN*] \ [*PART ID*] \ [*JPEG FILE*]

  검사) [*BOARD ID*] \ [*CLASSIFY*] \ [*PART ID*] \ [*JPEG FILE*]

- [BOARD ID] 이후의 경로는 입력하지 않아도 학습/검사가 모두 이루어짐

- 파일 확장자 : **JPEG**
- 파일 이름 지정 규칙 : [*CATEGORY*].jpeg
  - 오류 이미지 파일 이름 예시/규칙 : ```103.jpeg```/카테고리 100번 이후로 시작은 오류 이미지
  - 정상 이미지 파일 이름 예시/규칙 : ```3.jpeg```/카테고리 1번부터 시작은 정상 이미지
### Output

- 뉴런 수와 벡터 길이가 서로 다른 4가지 모드를 검사하고 출력
- 뉴런 수와 벡터 길이는 조정 가능하며 하드웨어 성능 제한에 의하여 ```512x32```, ```256x64```, ```128x128```, ```64x256``` 4가지 옵션으로 설정 가능
- 출력 옵션은 ```Board_id```, ```Part_id```, ```Algorithm```, ```Accuracy``` 총 4가지
- ```Board_id``` : 검사할 보드의 종류/명칭
- ``Part_id`` : 검사할 부품의 종류/명칭
- ```Algorithm``` : 검사 알고리즘 종류로 Color 또는 Corner로 구분
- ```Accuracy``` : 검사 후 정확도(%)
- ```Color``` 알고리즘의 경우, 총 4가지 경우의 수를 모두 출력하지만 ```Corner``` 알고리즘의 경우 벡터 길이를 32, 64를 출력. ```Corner``` 알고리즘의 특성상 벡터 길이가 64를 초과하지 않기 때문
- 검사 결과를 JSON 파일로 저장

####   Output Example

```
---------------------------------------
case1) neurons/vectors = " 512 / 32 "
---------------------------------------
Board_id  Part_id  Algorithm  Accuracy
 HC-06      1871      Color      85
 HC-06      1872      Color      76
 HC-06      1873      Color      83
 HC-06      1874      Color      68
 ...
 HC-06      1871      Corner     91
 HC-06      1872      Corner     45
 HC-06      1873      Corner     68
 HC-06      1874      Corner     73
 ...
---------------------------------------
case2) neurons/vectors = " 256 / 64 "
---------------------------------------
Board_id  Part_id  Algorithm  Accuracy
 HC-06      1871      Color      67
 HC-06      1872      Color      83
 HC-06      1873      Color      54
 HC-06      1874      Color      66
 ...
 HC-06      1871      Corner     54
 HC-06      1872      Corner     91
 HC-06      1873      Corner     72
 HC-06      1874      Corner     37
 ...
---------------------------------------
case3) neurons/vectors = " 128 / 128 "
---------------------------------------
Board_id  Part_id  Algorithm  Accuracy
 HC-06      1871      Color      28
 HC-06      1872      Color      49
 HC-06      1873      Color      53
 HC-06      1874      Color      76
 ...
---------------------------------------
case4) neurons/vectors = " 64 / 256 "
---------------------------------------
Board_id  Part_id  Algorithm  Accuracy
 HC-06      1871      Color      35
 HC-06      1872      Color      58
 HC-06      1873      Color      90
 HC-06      1874      Color      68
 ...
```

####   JSON Example

```
{
  "objective": "Component Inspection",
  "Board Name": "HC-06",
  "algorithm": [
    "color": [
      {
        "part_id": 10002311,
        "number of neurons": 512,
        "vector length": 32,
        "accuracy": 0.91
      },
      {
        "part_id": 10002312,
        "number of neurons": 512,
        "vector length": 32,
        "accuracy": 0.93       
      },
      {
        ...
      },
      {
        "part_id": 10002311,
        "number of neurons": 256,
        "vector length": 64,
        "accuracy": 0.83
      },
      {
        "part_id": 10002312,
        "number of neurons": 256,
        "vector length": 64,
        "accuracy": 0.76       
      },
      {
        ...
      }
    ],
    "corner": [
      {
        "part_id": 10002311,
        "number of neurons": 512,
        "vector length": 32,
        "accuracy": 0.95     
      },
      {
        "part_id": 10002312,
        "number of neurons": 512,
        "vector length": 32,
        "accuracy": 0.83       
      },
      {
        ...
      },
      {
        "part_id": 10002311,
        "number of neurons": 256,
        "vector length": 64,
        "accuracy": 0.89     
      },
      {
        "part_id": 10002312,
        "number of neurons": 256,
        "vector length": 64,
        "accuracy": 0.74       
      },
      {
        ...
      }
    ]
  ]
}
```

####    Simulator Example

![Simulator example](https://user-images.githubusercontent.com/35215836/121492267-b2537200-ca11-11eb-85e0-0feef1e28eb7.png)
![image](https://user-images.githubusercontent.com/35215836/121494350-a10b6500-ca13-11eb-9c73-d4dc0202f10d.png)
