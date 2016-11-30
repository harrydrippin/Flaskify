# Flaskify
Simple Python library for super-fast API building and sharing for purpose of hackathon.

[Here](https://github.com/harrydrippin/Flaskify/blob/master/README_en.md) is README file for English users.

### 개요

이 프로젝트는 (사)앱센터에서 진행하는 [Startup Weekend](http://appcenter.kr/archives/category/startupweekend)에서 개발된 도구로, 해커톤에서 Flask 기반 Service Back-end API를 만들고자 할 때 빠르게 구조를 정리하여 기초적인 Skeleton Code를 만들고 그 내용을 `.md` 포맷으로 출력해 팀원 공유하거나 Github 위에서 관리할 수 있게 해주는 Python 기반의 도구입니다.

_현재 개발이 진행되고 있는 프로젝트로, 아직 불안정할 수 있습니다._

### 사용법

단일 `.py` 형식 코드로 제공되며, 용례는 다음과 같습니다.

```shell
python flaskify.py <JSON file>  # 기본 사용 방법 (디렉토리에 app.py 파일 생성)
python flaskify.py <JSON file> -c  # 코드에 주석으로 TODO Memo를 덧붙임
python flaskify.py <JSON file> -m  # Markdown 문법으로 API Document를 출력함
```

### 오픈소스 라이센스

본 프로젝트는 MIT License 하에 개발 및 배포됩니다. 출처를 밝히는 한, 상업적 용도로의 사용이나 수정, 배포가 가능합니다.