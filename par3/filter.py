import markdown

def format_datetime(value, fmt='%Y-%m-%d %H:%M'):
    return value.strftime(fmt)

# 마크다운 변환 함수 선언  
def format_markdown(text):
    if not text:
        return ""
    # markdown.markdown()의 결과(문자열)를 MarkupSafe의 Markup 객체로 감싸줍니다.
    # 이렇게 감싸주어야 템플릿(HTML)에서 꺾쇠 태그가 무력화되지 않고 화면에 잘 나옵니다.
    html_content = markdown.markdown(text, extensions=['nl2br', 'fenced_code', 'sane_lists', 'tables'])