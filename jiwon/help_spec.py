import os 
from openai import AzureOpenAI
import base64
import requests

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "./test_image.jpg"
base64_image = encode_image(image_path)


api_base = "https://kic-2024-openai.openai.azure.com/"
api_key= ""
deployment_name = 'af618f92-ebde-4e5a-9f71-3a1b8826f341'
api_version = '2023-07-01-preview'

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)

prompt = ""

sum = input('발명 요약 : ')

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": "당신은 전문적인 변리사입니다. 특허를 출원하기 위한 특허 명세서 작성을 합니다. 문법, 문장 구조와 문서 형식에 엄격합니다." },
        { "role": "assistant", "content" : 
            """Knowledge : 
            <특허 명세서의 구성> \n
    [발명의 명칭] \n 발명의 내용을 간명하게 표시할 수 있는 발명의 명칭을 기재하여야 하며, 영문 명칭을 {{}}안에 다음 예와 같이 입력하여야 합니다. [예] [발명의 명칭] 자동차용 범퍼{{AUTOMOBILE BUMPER}}
    [기술분야] \n 발명의 기술 분야를 서술하세요. [예] 본 발명은 ㆍㆍㆍ하기 위한 ㆍㆍㆍ에 관한 ㆍㆍㆍㆍㆍㆍ.
    [배경기술] \n 출원하고자 하는 기술이 속하는 분야에서 종래에 있었던 기술을 설명함으로서 출원내용의 장점을 설명하세요
    [발명의 내용] 
        1. [해결하려는 과제] \n 발명이 과제로 하고 있는 종래 기술의 문제점 등을 기재합니다
        2. [과제의 해결 수단] \n 발명에 의하여 어떻게 해당 과제가 해결되었는지를 기재합니다
        3. [발명의 효과] \n 발명이 종래 기술과 비교하여 우수하다고 인정되는 사항을 서술합니다, 발명에 따라 기대되는 효과를 작성하세요
    [발명을 실시하기 위한 구체적인 내용] \n 중요한 권리 부분으로 보호받고자하는 기술 내용 설명하는 부분입니다. 발명의 구성을 도면과 관련하여 번호를 붙여가며 각각의 역할을 자세히 서술하세요.
    [특허청구의 범위] \n 보호받고자 하는 기술내용의 요약을 포함하는 청구항을 구체적으로 작성하세요. 각 청구항은 항마다 행을 바꾸어 기재하고, 기재하는 순서에 따라 숫자로 번호를 붙여야 합니다.
    [도면의 간단한 설명] \n 첨부되는 도면의 종류([예] 사시도, 단면도 등)을 간단히 언급하시오. [예] 도 3은 본 발명에 따른 단말기의 사시도"""},
        
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": 
                f"""

이미지는 발명하려 하는 발명품의 도면입니다.
제시되는 도면 이미지와 발명 요약을 기반으로 특허 명세서를 작성해주세요. 특허 명세서의 형식은 <특허 명세서의 구성>을 따라서 작성해주세요.

Context :
- 발명 요약 : {sum}

결과는 <특허 명세서 구성>의 bullet point 형식을 따른 특허 명세서만 출력하세요. ( '-'는 사용하지 말 것) bullet point 마다 \n 를 추가해서 출력하세요.
"""
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ] } 
    ],
    max_tokens=4096
)

print(f"[발명 요약] \n {sum}", "\n", response.choices[0].message.content)