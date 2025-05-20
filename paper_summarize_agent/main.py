import os
from dotenv import load_dotenv

from openai import OpenAI
from glob import glob
from extract_pdf_ieee import extract_IEEE_paper_contents

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

def summarize_paper(file_path: str):
    client = OpenAI(
        api_key=API_KEY
    )

    # todo: check type of paper. ex) is IEEE, or XX

    summarized_txt = extract_IEEE_paper_contents(file_path)

    system_prompt = f'''
    너는 논문 pdf 파일에서 추출된 글을 상세히 분석하는 봇이야.
    추가로 다음의 규칙을 따라 --- 아래의 글을 분석해줘.

    1번 규칙
        **각 섹션의 제목**
        내용은 가독성이 좋게 정리

    2번 규칙
        Method 섹션은 다른 섹션보다 더 상세히 분석하고, 수식은 LaTex문법으로
    
    3번 규칙
        결과 섹션에서 보여주는 정량적 결과는 빠트리지말고 정리해줘
    
    ---
    {summarized_txt}
    '''

    print(system_prompt)
    print('========================')


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature= 0.1, 
        messages=[
            {
                "role": "system", 
                "content": system_prompt
            }
        ]
    )

    return response.choices[0].message



if __name__ == "__main__":
    pdf_file_path = glob(os.path.join('pdf','ieee', '*.pdf'))[0]
    pdf_file_name = os.path.basename(pdf_file_path)
    pdf_file_name = os.path.splitext(pdf_file_name)[0]
    
    txt_file_path = os.path.join(os.getcwd(), f'summarized_{pdf_file_name}.txt')
    
    summarized_txt = summarize_paper(pdf_file_path)

    # save summarized txt to file
    if summarized_txt:
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(summarized_txt)
