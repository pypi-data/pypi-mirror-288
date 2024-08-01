## VridgeAI package  
- 최신 버전: 0.1.2

<br>

## 진행 상황

- 조직, 프로젝트 모델 조회 
- Dataset 업로드 
- 통계 정보 저장 
- 모델 다운로드 

<br>

### 조직, 프로젝트 모델 조회 

```python
from vridgeai import vridgeai_utils 

api_key = "bf47a560-d8d2-411b-957b-1e8b3036369f"
orgId = "2f0e2dc9433c46b1b21f81fdc3258fe6"
projectId = "p-rkxbu51xz4fs"

# 프로젝트 모델을 조회한다면 id=projectId, for_project()
model_check = vridgeai_utils.ModelCheck(api_key, projectId)
response = model_check.for_project()

# 반대로 조직 모델을 조회한다면 id=orgid, for_organization()
model_check = vridgeai_utils.ModelCheck(api_key, orgId)
response = model_check.for_organization()
```

<br>

### Dataset 업로드 

```python
from vridgeai import dataset_utils

uploader = dataset_utils.DatasetUploader(projectId, orgId, api_key)
response = uploader.dataset_upload()
# print(response)
```

<br> 


### 통계 정보 저장 

```python 
from vridgeai import model_utils

saver = model_utils.StatInfoSaver(api_key)
response = saver.save_stat_info()
```

<br> 

### 모델 다운로드 

```python
from vridgeai import model_utils

file_name = "model_download"
model_utils.ModelDownloader(key, file_name)
```
- file_name: 다운로드 할 파일 이름 

```commandline
C:.
├───.idea
│   └───inspectionProfiles
├───download_folder
└───__pycache__

```

모델 다운로드 경로는 download_folder. 
- 만약 폴더가 없다면 생성 후 모델 다운로드 
- 다운로드 형식은 <file_name>.zip