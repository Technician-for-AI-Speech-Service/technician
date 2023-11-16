실행가이드

- 환경구축

1) 사용 환경 툴 : Visual Studio (+Anaconda)

2) 설치 툴 및 라이브러리
    1. 설치 툴 : Python, MySQL Workbench, Microsoft C++ Build Tools
    2. 라이브러리(Visual Studio) : pip-packages, pyproject.html snippets, MySQL, MySQL Shell for VS Code, mysqlconnector, PowerShell, PowerShell, PowerShell Snippets

3) DB연결 (MySQL 연결) : MySQL Workbench 창 - MySQL Connections (+) 클릭 - Setup New Connection 정보 입력 - Test Connection 버튼 클릭 - Success 창(연결성공 창) 확인

    ***입력정보**
     (1) HOST : 'project-db-stu3.smhrd.com'
     (2) PORT : 3307
     (3) USER : 'Insa4_IOTB_final_3'
     (4) DB : 'Insa4_IOTB_final_3'
     (5) Password : aischool3'

4) 실행 방법
   1. Terminal 창 열기 (메뉴바 Terminal - New Terminal)
   2. Python 3. 11 버전 이하 선택(Select Interpreter 경로에서 Python 선택)
   2. app.py 창 실행(터미널 환에서 ctrl + F5)

  
5) 에러발생 관련 환경설정 구축
   1. conda path 경로 에러 : **OS환경에서 시스템 - 고급시스템 설정 - 환경변수 - Path 편집 클릭 - 파이썬경로 추가**

* 파이썬 경로 3개 추가(C:\Users\AppData\Local\Programs\Python\Python312, C:\Users\AppData\Local\Programs\Python\Python312\Lib, C:\Users\AppData\Local\Programs\Python\Python312\Scripts)
* 해당경로에 파이썬 폴더가 없다면 파이썬 설치가 안 되어있으므로 설치해야함.
 
ex) conda : The term 'conda' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path wa
s included, verify that the path is correct and try again.
At line:1 char:1
+ conda activate base

  2. pip 에러, pyproject 에러 : **Extensions 환경툴 설치창에서 필요한 툴 설치 필요**

* 필요한 툴 : pip-packages, pyproject.html snippets 설치
* 기타 툴 : MySQL, MySQL Shell for VS Code, mysqlconnector, PowerShell, PowerSheel Snippets
 
ex) pip : The term 'pip' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was in
cluded, verify that the path is correct and try again.

ex) ERROR: Could not build wheels for mysqlclient, which is required to install pyproject.toml-based projects
  
  3. import 에러 : **Terminal 창에서 "pip install '라이브러리'" 입력하고 설치**

* 라이브러리 예) flask_mysqldb, flask_login

ex) Exception has occurred: ModuleNotFoundError
No module named 'flask_mysqldb'
  File "C:\Users\user\Desktop\Front-end-front_end_v1\app.py", line 2, in <module>
    from flask_mysqldb import MySQL
ModuleNotFoundError: No module named 'flask_mysqldb'


4. mysqlclient 에러 :
   (1) mysql db연결(MySQL Workbench에서 db생성하고 연결하기)
   (2) Terminal 창에서 **pip install mysqlclient, pip install --upgrade pip setuptools wheel, pip install pymysql** 실행
   
 
ex)  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for mysqlclient
Failed to build mysqlclient
ERROR: Could not build wheels for mysqlclient, which is required to install pyproject.toml-based projects

5. Microsoft Visual C++ 에러 : Microsoft C++ Build Tools 설치

   * 설치사이트 Link : **https://visualstudio.microsoft.com/visual-cpp-build-tools/**
   * 툴 설치후 도구설치 : 워크로드에서 '데스크톱 및 모바일' - C++를 사용한 데스크톱 개발 및 기타 필요한 도구들 설치 

ex) error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

6. watchdog Import 에러 :
   ImportError: cannot import name 'EVENT_TYPE_OPENED' from 'watchdog.events' 발생시
   watchdog 삭제 후 재설치
   (1) pip uninstall watchdog
   (2) pip install watchdog
   
