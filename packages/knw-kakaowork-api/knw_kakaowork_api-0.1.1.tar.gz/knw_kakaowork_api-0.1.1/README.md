# 케이앤웍스 카카오워크 API
<br>
개발자 : archon.oh (knworks)

## 알림 API 

### \# **인스톨**<br>
```python
pip install knw-kakaowork-api
```

### \# **모듈 임포트**<br>
```python
import knw_kakaowork_api
```
<br>

### \# **Info 함수**<br>
```python
knw_kakaowork_api.Info(codename='APY001', msg='여기에 메시지 입력', email_adress_list=['archon@knworks.co.kr'],api_key='as123ras23g')
```
- codename: 과제명(코드) ,
- msg: 텍스트 메시지 내용 ,
- email_adress_list: 수신자 이메일주소(리스트형태로 다수 발송가능) ,
- api_key: Bot 생성 시 인증키
<br><br>
![Info 결과](https://github.com/user-attachments/assets/c1e12754-694b-4229-87b2-b2eeed4a7ed6)


### \# **Success 함수**<br>
```python
knw_kakaowork_api.Success(codename='APY001', msg='여기에 메시지 입력', email_adress_list=['archon@knworks.co.kr'],api_key='as123ras23g')
```
- codename: 과제명(코드) ,
- msg: 텍스트 메시지 내용 ,
- email_adress_list: 수신자 이메일주소(리스트형태로 다수 발송가능) ,
- api_key: Bot 생성 시 인증키
<br><br>
![Success 결과](https://github.com/user-attachments/assets/e0230c11-d4fd-4ad0-a345-93faea79572e)


### \# **Error 함수**<br>
```python
knw_kakaowork_api.Error(codename='APY001', msg='여기에 메시지 입력', email_adress_list=['archon@knworks.co.kr'],api_key='as123ras23g')
```
- codename: 과제명(코드) ,
- msg: 텍스트 메시지 내용 ,
- email_adress_list: 수신자 이메일주소(리스트형태로 다수 발송가능) ,
- api_key: Bot 생성 시 인증키
<br><br>
![Error 결과](https://github.com/user-attachments/assets/674afe8f-de84-4d36-ac84-c5aacb9b1c40)


### \# **txt 함수**<br>
```python
knw_kakaowork_api.txt(text='여기에 메시지 입력', email_adress_list=['archon@knworks.co.kr'], api_key='as123ras23g')
```
- text: 텍스트 메시지 내용 ,
- email_adress_list: 수신자 이메일주소(리스트형태로 다수 발송가능) ,
- api_key: Bot 생성 시 인증키
<br><br>
![txt 결과](https://github.com/user-attachments/assets/0ae48fd3-fea9-4325-82bc-c7c0347a0dd5)

