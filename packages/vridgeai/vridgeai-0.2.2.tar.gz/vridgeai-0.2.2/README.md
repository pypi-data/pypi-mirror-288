## vridageai docs  
- 최신 버전: 0.2.1
- 파이썬 버전: 3.9.0 


[파이썬 패키지 확인 링크 PyPI](https://pypi.org/project/vridgeai/0.2.1/)

<br>

## 기본 세팅
```python
import requests
import zipfile
import numpy as np
import os
import json
import tensorflow as tf

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
orgId = os.getenv("orgId")
projectId = os.getenv("projectId")
```
모든 코드들은 위와 같이 import 되어 있다고 가정합니다. 
- **`.env` 파일을 생성한 후 문서를 참고하세요.**

<br>

### 조직, 프로젝트 모델 조회 방법 
조직과 프로젝트 모델을 조회하는 방법은 다음과 같습니다. 
```python
from vridgeai import model_utils

model_utils.GroupModelCheck(api_key, orgId)
```

<br>
GroupModelCheck 클래스는 구조는 같습니다. 

필요

- **for_organization**: 조직 모델을 조회합니다.


