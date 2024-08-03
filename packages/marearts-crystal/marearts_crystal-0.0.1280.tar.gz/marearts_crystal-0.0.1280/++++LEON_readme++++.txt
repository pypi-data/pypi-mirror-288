

파일 구조

marearts-crystal/
├── .github/
│   └── workflows/
│       └── build_and_publish.yml
├── marearts_crystal/
│   ├── __init__.py
│   └── ma_crystal.pyx
├── tests/
│   └── test_ma_crystal.py
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.cfg
├── setup.py
├── deploy.sh
└── requirements.txt


배포 할때는 다음을 실행, push -> github -> github action -> build win,mac,linux -> pypi deployment
./deploy.sh

개발 과정
ma_crystal_origin_code.py 으로 개발을하고
./marearts_crystal/ma_crystal.pyx를 업데이트 하자
so file을 로컬에서 빌드해서 다음 테스트 파일을 실행해서 체크한다
./test/example.py



pip install check-manifest
check-manifest