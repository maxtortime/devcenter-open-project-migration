# nforge-migration

[![Build Status](https://travis-ci.org/naver/devcenter-open-project-migration.svg?branch=master)](https://travis-ci.org/naver/devcenter-open-project-migration)
[![PyPI](https://img.shields.io/pypi/dm/nforge-migration.svg)]()
[![PyPI](https://img.shields.io/pypi/v/nforge-migration.svg)]()
[![PyPI](https://img.shields.io/pypi/l/nforge-migration.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/nforge-migration.svg)]()

네이버 개발자센터 오픈 프로젝트 백업 및 마이그레이션을 위한 Python 모듈입니다. 본 모듈은 [네이버 개발자센터의 오픈 프로젝트](http://dev.naver.com/projects) 의 마이그레이션을 위해 2가지 기능을 제공합니다.
1. 네이버 오픈프로젝트 백업: 로컬PC에 개인의 오픈 프로젝트 데이터 (이슈/게시판/첨부 파일 포함)를 백업
2. Github로 마이그레이션: 로컬PC에 백업한 데이터를 GitHub의 프로젝트로 마이그레이션

## 설치/실행 환경
본 모듈은 CLI(Comamnd Line Interface) 형태의 모듈로서 Windows, Mac, Linux OS를 모두 지원하며, 아래 버전 이상의 프로그램이 설치되어 있어야 합니다.

1. Python 2.7 이상 ( 커맨드 라인에서 Python 버전확인 방법: `$ python --version`)

2. Git 1.7.10 이상  ( 커맨드 라인에서 Git 버전확인 방법: `$ git --version`)

3. pip 7 이상 ( 커맨드 라인에서 pip 버전확인 방법: `$ pip --version`)

위 3가지 프로그램이 없을 경우는 아래의 가이드를 따라 설치해주시길 바랍니다.

### Python 설치
  * [Windows에서 Python 설치법](https://wikidocs.net/8) (**"Add Python 3.5 to PATH"** 설치시 반드시 이 옵션을 체크하세요)
  * Mac, Linux: 기본적으로 Python이 제공됩니다.

    > python --version (버전 확인 방법)

    위 명령어 실행 시 2.7버전 이상이 아니신 분은 [이 자료](http://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_Python_2.7_%EC%BB%B4%ED%8C%8C%EC%9D%BC_%EC%84%A4%EC%B9%98)를 참고하셔서 업그레이드 하길 바랍니다.

### [Git 설치](https://help.github.com/articles/https-cloning-errors/#check-your-git-version)
> 이 버전 미만일 경우 GitHub에 push가 불가능해서 첨부파일 마이그레이션이 불가능합니다.

  * Windows 에서는 Git 공식 홈페이에서 적절한 Git 설치 파일을 [다운로드](https://git-scm.com/download/win) 받아 설치하시면 잘 동작합니다.
  * 대부분 유닉스 계열에서 Git 1.7.10 이상을 지원합니다.

    ```sh
    $ sudo apt-get install git # 데비안 계열
    $ sudo yum install git # 페도라 계열
    $ brew install git # OSX
    ```
  * 간혹 CentOS 6를 이용하시는 분은 기본 yum 저장소에 있는 Git 버전이 낮아 GitHub에 Push가 안 되는 오류가 일어날 수 있습니다. [이 자료](http://maxtortime.github.io/the-post-6832/)를 참고하셔서 Git 버전을 업그레이드 해주세요.

### pip 설치
#### Windows
- 위의 설치법을 따라하셨다면 pip가 자동으로 설치되있을 것입니다. 그러나 `pip --version` 을 실행하셨을 때 오류가 발생하신다면 아래 과정을 따라해주세요.
  1. https://bootstrap.pypa.io/get-pip.py 파일을 다운로드하세요.
  2. `$ python get-pip.py`
  3. pip 설치 버전 확인: `$ pip --version`

- 간혹 위 과정을 따라하셨는데도 `pip`를 실행할 수 없는 경우는 시스템 속성의 환경변수 편집하는 곳에서 시스템 변수의 `PATH`에 파이썬 설치 경로를 추가해주세요.

#### Linux/Mac OS
  1. pip 설치 스크립트 다운로드: `$ curl https://bootstrap.pypa.io/get-pip.py > get-pip.py`
  2. pip 설치: `$ sudo python get-pip.py`
  3. pip 설치 버전 확인: `$ pip --version`

## 모듈 설치 방법
python, git, pip가 설치되었으면 다음의 명령어를 입력하여 모듈을 설치합니다.   

### Linux, Mac 사용자
아래의 명령어만 입력하면 마이그레이션 모듈이 설치됩니다.
`$ pip install nforge_migration`

### Windows 사용자
1. Lxml (XML 파서) 설치파일 다운로드
   - 자신의 파이썬 버전과 운영체제에 맞는 설치파일을 다운로드해주세요.
   - Python 2.7 [32 bit](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp27-cp27m-win32.whl) [64 bit](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp27-cp27m-win_amd64.whl)
   - Python 3.4 [32 bit](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp34-cp34m-win32.whl) [64 bit](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp34-cp34m-win_amd64.whl)
   - Python 3.5 [32 bit](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp35-cp35m-win32.whl) [64 bit](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp35-cp35m-win_amd64.whl)

2. Lxml (XML 파서) 설치 `$ pip install (다운로드한 파일명)`

3. 마이그레이션 모듈 설치
`$ pip install nforge_migration`


### 마이그레이션 모듈 소스를 이용한 직접 설치
- `pip install nforge_migration` 명령어를 이용하지 않고, 본 프로젝트의 소스를 이용해서 직접 설치할 수도 있습니다.

  ```
  $ git clone https://github.com/naver/devcenter-openproject-migration.git
  $ cd devcenter-openproject-migration
  $ sudo pip install -e .
   ```

### 설치 완료 확인
- `npa --help` 명령어를 입력하셨을 때 아래와 같은 화면이 보이면 설치가 완료된 것 입니다.

  ```sh
  Usage: npa [OPTIONS]

  Command line interface for parsing Nforge project.

  Options:
    --name TEXT  오픈 프로젝트 이름
    --private            오픈 프로젝트 비공개 저장소 여부
    --dev_code           DevCode 프로젝트인지
    --help               Show this message and exit.
  ```
- 설치 완료 후 작업을 위한 폴더를 만들어주세요.


## 모듈 사용 방법    
본 모듈은 아래 2가지 기능을 제공합니다.

1. 네이버 오픈프로젝트 백업

  로컬PC에 개인의 오픈 프로젝트 데이터 (이슈/게시판/첨부 파일 포함)를 백업
2. Github로 마이그레이션

  로컬PC에 백업한 데이터를 GitHub의 프로젝트로 마이그레이션


- 주의 사항 !!
   - 네이버 오픈프로젝트가 `비공개` 상태이면 `공개`로 전환 후 진행하시거나, 프로젝트 관련 인증키값 데이터를 추출해 저장하신 다음 진행해야 합니다.
   - 비공개 프로젝트 관련 인증 키값 추출 방법
        1. [오픈 프로젝트](http://dev.naver.com/projects)에 로그인 해주세요.
        2.  웹브라우저 주소창에 직접 `javascript:document.cookie` 라고 입력하세요. ( Ctrl C / V 하시면 안됩니다.)
        3. 웹브라우저에 보이는 값들 중 `NID_SES`와 `NID_AUT` 값을 복사해주세요.
        4. 작업 폴더에 `cookies.txt` 라는 파일을 만들어주세요.
        5. 아래와 같은 형식으로 `cookies.txt` 파일을 채워주시고 저장하세요. (쿠키 값의 맨마지막 세미콜론은 지울 것)
        ```
        NID_SES=키값
        NID_AUT=키값
        ```

### 네이버 오픈프로젝트 백업
* `npa` 명령어를 아래의 안내와 같이 터미널에 입력해주세요.
    * 공개 프로젝트: `npa --name 프로젝트이름`
    * 비공개 프로젝트: `npa --name 프로젝트이름 --private`

* 자동으로 프로젝트들이 다운로드되고 아무 메시지 없이 끝났다면 성공한 것입니다.
```
Now making 7267.xml and 7267.json of download: 100%|███| 2/2 [00:01<00:00,  1.04s/it]
Now making 98439.xml and 98439.json of issue: 100%|███| 21/21 [00:09<00:00,  2.78it/s]
Now making 98483.xml and 98483.json of forum: 100%|███| 11/11 [00:02<00:00,  3.17it/s]
```
* `작업 폴더/Nforge/open_project/프로젝트 이름` 에 프로젝트들이 다운로드 됩니다. 폴더는 아래와 같은 구조로 구성되어 있습니다.

    ```
    Nforge
    └── open_project
        └── 프로젝트 이름
            ├── code_info.json # 소스 코드 저장소 정보가 담긴 파일
            ├── developers.txt # 개발자들의 네이버 아이디
            ├── downloads # 다운로드 저장 폴더
            │   ├── json
            │   ├── raw # 첨부파일
            │   └── xml
            ├── issues # 이슈/게시판 저장 폴더
            │   ├── json
            │   ├── raw # 첨부파일
            │   └── xml
            │       ├── forum # 게시판 XML
            │       └── issue # 이슈 XML
            └── milestones # 마일스톤 XML
    ```

### GitHub 마이그레이션
#### Github로 마이그레이션을 위한 조건
- GitHub 저장소 생성
- 해당 저장소에 위키 생성
- 해당 저장소에 대한 접근토큰값(Personal Access Token)

조건을 충족한 후 마이그레이션 명령어 수행을 위해 아래 안내를 차례대로 따라해주세요.

#### 마이그레이션 준비
1. [GitHub](https://github.com) 계정이 없는 분은 회원가입을 해주세요. **[참고](https://help.github.com/articles/signing-up-for-a-new-github-account/)**
2. [GitHub 저장소 import  링크로 이동](https://github.com/new/import/)  
3. `Your old repository’s clone URL` 에는 `오픈 프로젝트->코드` 탭에서 확인할 수 있는 `git clone` URL 혹은 `svn`의 URL을 입력하세요.
4. `Your new repository details` 아래에 `Name`에 생성될 저장소 이름을 입력하세요.
5. `Public/Private` 여부를 체크하고 `Begin import` 버튼을 눌러 시작하세요.
6. Import를 시작하게 되면 몇 초후 아이디와 비밀번호를 입력하는 폼이 보입니다.
    - 공개 프로젝트의 경우: 아이디/비밀번호 모두 `anonsvn` 입력
    - 비공개 프로젝트의 경우: 네이버 아이디와 비밀번호
5. 소스 코드 저장소 마이그레이션이 끝나면 GitHub에 등록하신 메일로 완료 안내가 갑니다.
6. 메일을 받으신 후 아래 안내를 참고하셔서 위키와 접근토큰값을 만들어주세요.

#### 저장소 Wiki 생성
1. https://github.com/사용자아이디/프로젝트명/wiki 로 접속해서 `Create the first page` 버튼 클릭
2. 페이지 우측 하단에 `Save Page` 버튼 클릭


#### Personal Access Token 생성
1. https://github.com/settings/tokens 으로 이동
2. 우측 메뉴 상단에 `Generate new token` 버튼 클릭
3. 아래 항목들을 입력
    - `Token Description` (토큰 설명, 예: `openproject`)
    - 체크박스들 중에 `repo` 항목에 체크
4. 하단에 `Generate token` 버튼 클릭 후 나오는 코드값을 복사
5. 작업 폴더에 `token.txt` 라는 파일을 만들고 복사한 토큰을 넣어준 후 저장한다.

#### 마이그레이션 명령어 수행
- 본인의 계정에 바로 마이그레이션 하는 경우
  - `ghm --name GitHub저장소이름 --project_name 오픈프로젝트이름`
- 특정 Organization의 저장소에 마이그레이션 하는 경우
  - `ghm -name GitHub저장소이름 --project_name 오픈프로젝트 이름 --org_name Organization이름` 
- `오픈프로젝트이름` 은 위에서 다운로드한 오픈 프로젝트 이름과 일치해야 합니다.
- `GitHub저장소이름` 은 위에서 만드신 저장소 이름과 일치해야 합니다.


  ```
   a8b9g3q9c... is valid token # 토큰 검증
   53%|█| 17/32 [00:17<00:16,  1.11s/it] # 이슈 업로드
   ... # Git 메시지 (이슈 첨부파일 업로드 과정)
   100%|███| 2/2 [00:08<00:00,  5.34s # 다운로드 마이그레이션
  ```
- 위 과정을 거친 후 아무 에러메시지 없이 끝났다면 성공한 것입니다.

### 주의사항
* 빠른 시간 내에 많은 GitHub 마이그레이션을 수행하면 [Abuse Rate Limits](https://developer.github.com/v3/#abuse-rate-limits)가 발생해 일시적으로 GitHub API를 호출할 수 없게 됩니다. 몇 분 후에 다시 시도해주세요.
* github에 위키를 만들지 않았을 경우 첨부파일이 누락될 수도 있으니 반드시 위키를 먼저 만드시길 바랍니다.
* 프로젝트 홈에 있는 문서 및 작성하신 위키는 마크다운(.md) 파일로 변환되어 [GitHub Wiki](https://help.github.com/articles/about-github-wikis/)에 저장됩니다. 원본파일에서 확장자만 바꾼 것이므로 기본적으로 마크다운을 사용하는 GitHub 위키에서 글을 확인할 때 렌더링이 잘못 되어 보일 수 있습니다.
* 프로젝트 정보 및 로고 마이그레이션은 지원하지 않습니다.
* 개발자 명단 마이그레이션은 지원하지 않습니다.

## 마이그레이션 결과 확인 방법

### 게시판/이슈 마이그레이션 확인
* 모두 [GitHub Issue](https://guides.github.com/features/issues/)로 옮겨집니다. 라벨을 통해 이슈/게시판 분류를 확인할 수 있습니다. 해결/닫힘인 이슈들은 `closed` 이슈, 해결중인 이슈들은 `open` 이슈로 분류됩니다.
* 아래와 같은 형식(마크다운)으로 이슈/게시판/댓글 이 옮겨집니다.
 ```markdown
 This {issue OR comment} created by **{작성자}** and assigned to **{담당자}** | {작성시간}

 ------
 {이슈 본문}
 -----
 ### Attachments
 * {첨부파일명}

 	![{첨부파일명}]({첨부파일링크})
 	...
 ```
* 이슈/게시판의 첨부파일은 GitHub 위키 저장소에 저장됩니다.

### 마일스톤
* 마일스톤 명단은 GitHub 이슈의 마일스톤으로 옮겨집니다.
* 마일스톤이 어느 이슈에 링크되었는지 여부는 지원하지 않습니다.

### 코드
* 프로젝트의 git/SVN 저장소가 GitHub로 옮겨집니다.
* GitHub는 SVN 방식의 디렉토리 구조를 따르지 않으므로 GitHub에서 저장소 구조가 조금 달라보일 수 있습니다.
* [GitHub에서 SVN 클라이언트 이용하기](https://help.github.com/articles/support-for-subversion-clients/)

### 다운로드
* 반드시 소스 코드 저장소 마이그레이션 후 수행하셔야 합니다.
* [GitHub의 Releases](https://help.github.com/articles/about-releases/)로 옮겨집니다.
* 버전 라벨이 원래 프로젝트와 조금 다를 수 있지만 순서는 일치합니다.
