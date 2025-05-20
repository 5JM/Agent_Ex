# AI Agent Practice (Paper Summarizer)

## Todo
[x] OpenAI API 연동

[x] Pdf 텍스트 추출 -> IEEE에 최적화

[] streamlit Web UI 연동


## 1. 논문 텍스트 추출
- `extract_pdf_ieee.py` 의 **extract_IEEE_paper_contents** 함수로 pdf 논문의 텍스트를 추출. (현재는 IEEE 형태에 최적화)

## 2. OpenAI Api를 활용해 논문 요약
- 개인 OpenAI Api key를 이용하여 논문 요약
- `GPT4o-mini`를 활용
-  `uv run main.py` 실행 및 생성된 txt파일 확인