import pymupdf, os, re
from glob import glob
from collections import defaultdict

def extract_IEEE_paper_contents(pdf_path):
    doc = pymupdf.open(pdf_path)
    content = []

    for page_idx, page in enumerate(doc):
        page_height = page.rect.height
        page_width = page.rect.width
        words = page.get_text("words")

        # 첫 페이지는 상단 20%, 나머지는 10%
        top_margin = 0.25 if page_idx == 0 else 0.1

        # 상하단 + 왼쪽 마진 제거
        words = [w for w in words if w[1] >= page_height * top_margin and w[3] <= page_height * 0.95]
        words = [w for w in words if w[0] >= page_width * 0.05]

        # 왼쪽/오른쪽 단 나누기
        left_words = [w for w in words if w[0] < page_width / 2]
        right_words = [w for w in words if w[0] >= page_width / 2]

        def group_words_to_lines(words_list):
            lines = defaultdict(list)
            for w in words_list:
                y_key = round(w[1] / 2)
                lines[y_key].append(w)
            sorted_lines = []
            for y in sorted(lines):
                line_words = sorted(lines[y], key=lambda w: w[0])
                line_text = ' '.join(w[4] for w in line_words)
                sorted_lines.append(line_text)
            return sorted_lines

        left_lines = group_words_to_lines(left_words)
        right_lines = group_words_to_lines(right_words)

        page_text = "\n".join(left_lines + right_lines)
        content.append(page_text)

    full_text = "\n".join(content)

    # 잡음 문구 제거
    noise_patterns = [
        r"IEEE.*?\n", r"DOI.*?\n", r"Authorized.*?\n", r"Download.*?\n", 
        r"Restrictions apply.*?\n", r"2025.*?\n", r"Page \d+ of \d+"
    ]
    for pattern in noise_patterns:
        full_text = re.sub(pattern, '', full_text, flags=re.IGNORECASE)

    # 섹션 경계 찾기
    lower_full_text = full_text.lower()
    abstract_start = lower_full_text.find("abstract")
    conclusion_start = lower_full_text.find("5. conclusion")
    references_start = lower_full_text.find("references")

    if abstract_start == -1 or conclusion_start == -1:
        print("Abstract 또는 Conclusion 섹션을 찾지 못했습니다.")
        return ""

    end_pos = references_start if references_start > conclusion_start else len(full_text)
    filtered_text = full_text[abstract_start:end_pos]

    return filtered_text.strip()

if __name__ == '__main__':
    pdf_file_path = glob(os.path.join('pdf','ieee', '*.pdf'))[0]
    pdf_file_name = os.path.basename(pdf_file_path)
    pdf_file_name = os.path.splitext(pdf_file_name)[0]
    
    txt_file_path = os.path.join(os.getcwd(), f'{pdf_file_name}.txt')
    

    filtered_paper = extract_IEEE_paper_contents(pdf_file_path)
    
    if filtered_paper:
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(filtered_paper)