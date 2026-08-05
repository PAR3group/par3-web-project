from werkzeug.security import generate_password_hash
# app과 db 객체가 정의되어 있는 파일에서 임포트해오세요.
from par3 import create_app, db
from par3.models import User

app = create_app()

with app.app_context():
    # 중복 생성 방지를 위해 이미 존재하는지 확인 (선택사항)
    existing_user = User.query.filter_by(user_id="testuser1").first()
    
    if not existing_user:
        # 테스트 유저 인스턴스 생성
        test_user = User(
            user_id="testuser1",
            nickname="테스터",
            password=generate_password_hash("1234"),  # 비밀번호 암호화 저장
            email="test@example.com",
            username="홍길동",
            phonenumber="010-1234-5678",
            user_sex="M",             # 성별 (예: 'M' 또는 'F')
            experience_years=3        # 경력 연수
        )
        
        # 데이터베이스 세션에 추가 후 커밋
        db.session.add(test_user)
        db.session.commit()
        print("테스트 유저가 성공적으로 생성되었습니다!")
    else:
        print("이미 해당 유저 ID가 존재합니다.")