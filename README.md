# cky-parser

## 설명

CKY parser를 이용한 문장을 parsing하는 프로그램입니다.

## Environment

* Windows 10 Pro
* python==3.8.1

## Requirements

* numpy==1.20.1

## 사용법

* `data/input.txt`에 parsing을 원하는 문장을 입력합니다.
    ``` md
    time flies like an arrow
    I saw a man on the hill with the telescope
    ...
    ```

* `main.py`를 실행합니다.
    ``` bash
    $ python main.py
    ```
    ```
    Input: time flies like an arrow
    (S (NP (n time))(VP (v flies)))
    (S (NP (n time))(VP (VP (v flies))(PP (P (p like))(NP (DT (det an))(NP (n arrow))))))
    (S (NP (n flies))(VP (v like)))
    (S (NP (n flies))(VP (VP (v like))(NP (DT (det an))(NP (n arrow)))))
    .
    .
    .
    ```

* `output.txt`와 `used_grammar.txt`에 각 문장에 대한 parsing 결과가 저장됩니다.