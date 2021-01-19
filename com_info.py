import requests
from io import BytesIO
import zipfile
import xmltodict
import json
import os
import csv


def findCompany_Info(name):
    code_list = []
    for item in data:
        if name in item['corp_name']:
            code_list.append(item['corp_code'])

    if not code_list: #결과가 없는 경우
        print('알맞은 데이터가 없습니다.')
        os.system('pause')
        os.system('cls')
        return
    elif len(code_list)>1: #결과가 2개 이상인 경우
        print(str(len(code_list))+'개의 결과가 검색되었습니다.\n')

        if len(code_list) >100: #100개가 넘는결과
            print('100개가 넘는 결과는 출력되지 않습니다.')
            os.system('pause')
            os.system('cls')
            return

        ans = input('출력하시겠습니까?(예/아니오)')
        if ans != '예':
            os.system('cls')
            return
            
        ans = input('사업자등록번호를 입력하시면 정확한 결과를 얻을 수 있습니다.(아니오: 0)\n')
        print('사업자등록번호가 맞지 않는다면 결과가 출력되지 않을 수 있습니다.')
        
    req = ['corp_name', 'ceo_nm', 'jurir_no','bizr_no','phn_no' ]
    req_kor = ['회사명', '대표자', '법인등록번호','사업자번호','전화번호']

    for code in code_list: #조건에 맞는 결과 출력
        res = requests.get(api_info +'?crtfc_key='+key+'&corp_code='+code)
        item = json.loads(res.text)

        if len(code_list)>1 and ans != '0' and ans != item['bizr_no']:
            continue

        for info in enumerate(req):
            print(req_kor[info[0]]+': '+item[info[1]]+'\n')
        info = (info for info in induty if info['index'] == item['induty_code'])
        print('업종: ' + str(next(info, {}).get('name')))

    os.system('pause')
    os.system('cls')
    
#(TODO)키스콘 면허정보 받아오기 


# DART FSS 기업 고유코드 zip파일 받기
key = input('액세스 키를 입력해주세요')
print('데이터를 받아오는중입니다.')
api_zip = 'https://opendart.fss.or.kr/api/corpCode.xml'
api_info = 'https://opendart.fss.or.kr/api/company.json'
res = requests.get(api_zip, params={'crtfc_key': key})
info_zip = zipfile.ZipFile(BytesIO(res.content))

data_xml = info_zip.read('CORPCODE.xml').decode('utf-8')
# odict: ordered dict
data_odict = xmltodict.parse(data_xml)
data_dict = json.loads(json.dumps(data_odict))
data = data_dict.get('result', {}).get('list')

#csv 업종코드 읽어오기
cf = open('induty_code.csv','r',encoding='CP949')
rdr = csv.reader(cf)
induty = list(dict())
for line in rdr:
    induty.append({'index':line[0],'name':line[1]})
cf.close()

# main
os.system('cls')
while True:
    print('='*50)
    print('키마다 하루에 검색할 수 있는 횟수가 제한되어있습니다.')
    print('프로그램 종료: x / 종료')
    print('='*50)
    company = input("기업명: ")
    if company == ('x'or'X') or company == '종료':
        break
    findCompany_Info(company)
