from datetime import datetime
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

def format_timeago(value):
    """24시간 이내면 'N시간 전' 등으로, 넘으면 날짜(YYYY.MM.DD)로 표시"""
    if not value:
        return ''

    now = datetime.now()
    diff = now - value
    seconds = diff.total_seconds()

    if seconds < 0:
        # 혹시 미래 시각이면 그냥 날짜로
        return value.strftime('%Y.%m.%d')
    elif seconds < 60:
        return '방금 전'
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f'{minutes}분 전'
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f'{hours}시간 전'
    else:
        return value.strftime('%Y.%m.%d')