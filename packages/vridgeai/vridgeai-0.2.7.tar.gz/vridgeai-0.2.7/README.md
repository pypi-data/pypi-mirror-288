## vridageai docs  
- 최신 버전: 0.2.7
- 파이썬 버전: 3.9.0 


[파이썬 패키지 확인 링크 PyPI](https://pypi.org/project/vridgeai/0.2.1/)

### 설치 방법 
```commandline
pip install vridgeai
```


<br>

## 시작하기
```python
import os
"""
Tenserflow GPU 설정 에러 무시 
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
orgId = os.getenv("orgId")
projectId = os.getenv("projectId")
key = os.getenv("key")
```
모든 코드들은 위와 같이 되어있다고 가정한 후 사용법을 설명합니다.
- **`.env` 파일을 생성한 후 문서를 참고하세요.**

<br>

### 만약 아래와 같은 에러가 발생한다면 다음 단계를 따르세요. 
```commandline
2024-08-01 17:15:07.443413: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2024-08-01 17:15:07.443577: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
```
[CUDA를 설치하세요.](https://developer.nvidia.com/cuda-11.0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exenetwork)

<br>

### 조직, 프로젝트 모델 조회 방법 
조직과 프로젝트 모델을 확인하기 위해 다음 단계를 따르세요.



```python
from vridgeai import model_utils

# 조직 모델 조회 
org_model = model_utils.GroupModelCheck(api_key, orgId)
org_model.for_organization()

# 프로젝트 모델 조회 
project_model = model_utils.GroupModelCheck(api_key, projectId)
project_model.for_project()
```

- model_utils에서 GroupModelCheck 인스턴스를 생성합니다. 

<br>

#### GroupModelCheck 인스턴스에 필요한 파라미터 

|   변수    |         설명         | 필수 여부 |
|:-------:|:------------------:|:-------:|
| api_key |      API KEY       | Y| 
| id | 조직 아이디 또는 프로젝트 아이디 | Y|

|                  id 설명                  | 
|:---------------------------------------:|
| `for_organization`: id가 orgId일 때 사용하세요. |
| `for_project`: id가 projectId일 때 사용하세요.  |

<br><br>

### 데이터셋 업로드 방법 
데이터셋을 업로드 하는 방법은 다음과 같습니다.

```python
from vridgeai import dataset_utils

uploader = dataset_utils.DatasetUploader(projectId, orgId, api_key)
uploader.dataset_upload()
```

<br>

#### DatasetUploader 인스턴스에 필요한 파라미터 

|   변수    |    설명    | 필수 여부 |
|:-------:|:--------:|:-------:|
| api_key | API KEY  | Y| 
| orgId |  조직 아이디  | Y|
| projectId | 프로젝트 아이디 | Y|

|                  설명                   | 
|:-------------------------------------:|
| `dataset_upload`: 데이터셋을 업로드할 때 사용하세요. |

<br><br>

### 통계 정보, Inference 정보 저장 
```python
from vridgeai import database_utils

saver = database_utils.SaveInformation(api_key)

saver.statistics()  # 통계 정보 저장 
saver.inference()  # inferenece 정보 저장
```

<br>

#### SaveInformation 인스턴스에 필요한 파라미터  

|   변수    |    설명    | 필수 여부 |
|:-------:|:--------:|:-------:|
| api_key | API KEY  | Y| 

|                   설명                    | 
|:---------------------------------------:|
|    `statistics`: 통계 정보를 저장할 때 사용하세요.    |
| `inference`: inference 정보를 저장할 때 사용하세요. |


<br><br>


### 모델 다운로드 
```python
from vridgeai import model_utils

# 모델 다운로드시 설정할 이름 
file_name = 'model_version_1'

model_utils.ModelDownload(key, file_name, True)
```

<br>

#### ModelDownload 인스턴스에 필요한 파라미터  

|   변수    |       설명        | 필수 여부 |
|:-------:|:---------------:|:-------:|
| key | 모델을 다운로드 받을 KEY | Y| 
| file_name | 모델 다운로드시 설정할 이름 | Y| 
| remove_zip_file |  .zip 파일 삭제 여부  | Y| 

|               remove_zip_file 설명                | 
|:-----------------------------------------------:|
|   `True`: 모델을 다운로드 받고난 후 생성된 .zip 파일을 삭제합니다.    |
| `False`: 모델을 다운로드 받고난 후 생성된 .zip 파일을 삭제하지 않습니다. |


<br><br>

### 모델 로드  
**위 모델 다운로드에서 파트에서 다운로드 받은 `model_version_1` 을 사용합니다.**
```python
from vridgeai import model_utils
from pathlib import Path

model_name = "model_version_1"  # 다운로드 받은 모델 이름 
project_folder_path = Path(__file__).parent  # 프로젝트 폴더의 경로 
ResNet = model_utils.Model(model_name, project_folder_path)
ResNet.load()  # 모델 로드 
```

<br>

#### Model 인스턴스에 필요한 파라미터  

|   변수    |          설명          | 필수 여부 |
|:-------:|:--------------------:|:-------:|
| model_name | 다운로드 받았을 때 설정한 모델 이름 | Y| 
| project_folder_path |    현재 프로젝트 폴더의 경로    | Y| 

<br>

### 모델 summary 출력 
```python
ResNet.summary() 
```
모델의 구조를 보고싶을 때 사용하세요. 


<br>

### 모델 추론값 출력 
```python
from vridgeai import data_preprocessing

image = "data.jpg"  # 이미지 경로
data = data_preprocessing.for_image(image)  # 이미지 데이터 전처리
```

#### data_preprocessing 인스턴스에 필요한 파라미터  

|         변수          |   설명   | 필수 여부 |
|:-------------------:|:------:|:-----:|
|        image        | 이미지 경로 |  Y    |



<br>

```python
ResNet.inference()  # 모델 inference 값 출력 
```
모델의 추론값을 아래와 같은 형식으로 출력합니다

```commandline
0 Accuracy: 0.366
1 Accuracy: 0.238
2 Accuracy: 0.118
3 Accuracy: 0.105
4 Accuracy: 0.133
5 Accuracy: 0.040
```