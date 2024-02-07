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


response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": "당신은 전문적인 변리사입니다. 특허를 출원하기 위한 특허 명세서 작성을 합니다. 문법, 문장 구조와 문서 형식에 엄격하세요" },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": 
                """
도면 이미지와 발명 요약을 기반으로 특허 명세서를 작성해주세요. 특허 명세서의 형식은 [특허 명세서의 구성]을 따라서 작성해주세요.

Context :

- 발명 요약 : 본 발명의 일 실시예에 따른 외부 기기와의 무선 통신을 수행할 수 있는 디지털 카메라에 있어서, 카메라 본체 및 카메라 본체에 장착되며, 복수의 촬영 렌즈들을 수용하는 복수의 배럴들을 가진 렌즈 배럴 조립체를 포함하며, 복수의 배럴들 중 어느 하나는 무선 통신을 위한 안테나 기능을 가진 안테나 배럴로 사용되며, 안테나 배럴이 안테나 기능을 수행하기 위한 전파를 방사할 수 있도록, 안테나 배럴은 금속 물질로 이루어지고 안테나 배럴에는 유전체 물질로 채워진 적어도 하나의 슬릿이 형성되며, 안테나 배럴의 외측 표면을 둘러싸는 카메라 본체의 외부 케이싱 부분은, 안테나 배럴의 그라운드로 기능하도록 금속 물질로 이루어지는 것을 특징으로 한다.
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

print(response.choices[0].message.content)