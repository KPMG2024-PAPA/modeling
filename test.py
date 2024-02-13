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
api_version = '2023-07-01-preview' # this might change in the future

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
        { "role": "system", "content": "당신은 전문적인 변리사입니다. 특허를 출원하기 위한 특허 명세서 작성을 합니다. 문법, 문장 구조와 문서 형식에 엄격하세요" },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": 
                f"""
도면 이미지와 발명 요약을 기반으로 특허 명세서를 작성해주세요. 특허 명세서의 형식은 [특허 명세서의 구성]을 따라서 작성해주세요.

Context :

- 발명 요약 : {sum}
- 특허 명세서의 구성
    1. 발명의 명칭 
    2. 특허청구의 범위 [보호받고자 하는 기술내용의 요약을 포함하는 청구항을 구체적으로 작성하세요]
    3. 발명의 효과 [발명에 따라 기대되는 효과를 작성하세요]
    4. 기술 분야 [발명의 기술 분야를 서술하세요]
    5. 배경 기술  [출원하고자 하는 기술이 속하는 분야에서 종래에 있었던 기술을 설명함으로서 출원내용의 장점을 설명하세요]
    6. 발명의 내용 [발명이 구현하고자 하는 목적과 해결점을 자세히 설명하세요]
        1. 해결하려는 과제
        2. 과제의 해결 수단 
        3. 발명의 효과
    7. 도면의 간단한 설명 [첨부되는 도면의 종류(ex. 사시도, 단면도 등)을 언급하시오]
    8. 발명을 실시하기 위한 구체적인 내용 [중요한 권리 부분으로 보호받고자하는 기술 내용 설명하는 부분입니다. 발명의 구성을 도면과 관련하여 번호를 붙여가며 각각의 역할을 자세히 서술하세요]

결과는 특허 명세서 구성의 bullet point를 따른 특허 명세서만 출력하세요.
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

print(f"- 발명 요약 : {sum} \n", response.choices[0].message.content)