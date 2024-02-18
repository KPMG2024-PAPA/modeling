import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.matplotlib.rcParams['font.family'] = 'AppleGothic'
from matplotlib.font_manager import FontProperties

import io
import base64

font_path_title = "./Pretendard-ExtraBold.ttf"
font_path_text = "./Pretendard-Medium.ttf"

ipc_application_category = pd.read_csv('./ipc_application_category.csv', index_col=0)

def ipc_category_graph(ipc_category: str) -> base64:
    
    
    """
    gpt_classifier에서 A01과 같이 반환 받아
    ipc_application_category.csv의 ipc_category에는 A만 입력해주게 됨.
    반환값으로 base64로 인코딩된 이미지를 반환합니다.

    """
    
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    
    custom_font_title = FontProperties(fname=font_path_title, size=20)
    custom_font_text = FontProperties(fname=font_path_text, size=10)
    
    # Plotting the time series data
    plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
    # plt.plot(ipc_application_category.index, ipc_application_category, marker='o', linestyle='-')  # Replace 'column_name' with the name of the column you want to plot

    # Plot each column
    for col in ipc_application_category.columns:
        if col[0] == ipc_category:
            plt.plot(ipc_application_category.index, ipc_application_category[col], label=col, marker='o', linestyle='-', color="#b57dfa")
        else: 
            plt.plot(ipc_application_category.index, ipc_application_category[col], label=col, linestyle='-', color="lightgrey")

    # Add labels and legend
    plt.xlabel('연도', fontproperties = custom_font_text)
    plt.ylabel('대분류별 출원 추이', fontproperties = custom_font_text)
    plt.xticks(fontproperties=custom_font_text)
    plt.yticks(fontproperties=custom_font_text)
    plt.title(f'대분류 {ipc_category} 특허 출원 추이',fontproperties = custom_font_title)
    plt.legend(prop = custom_font_text)
    # plt.grid(True)  # Add grid lines
    plt.text(1, -0.1, "참고: IPSS 지식 재산 통계 서비스", ha='right', fontproperties = custom_font_text, transform=plt.gca().transAxes)
    # Show plot
    # plt.show()
    
    img_bytes_io = io.BytesIO()
    plt.savefig(img_bytes_io, format='png')
    img_bytes_io.seek(0)
    plt.close()  # Close the plot to free up memory
    
    # Encode the image to base64
    img_base64 = base64.b64encode(img_bytes_io.getvalue()).decode()
    
    return img_base64


