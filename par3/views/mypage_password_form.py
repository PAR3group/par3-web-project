class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        '현재 비밀번호',
        validators=[
            DataRequired(message='현재 비밀번호를 입력해주세요.')
        ]
    )

    new_password = PasswordField(
        '새 비밀번호',
        validators=[
            DataRequired(message='새 비밀번호를 입력해주세요.'),
            Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다.'),
            Regexp(
                r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+|])[A-Za-z\d!@#$%^&*()\-_=+|]{8,}$',
                message='비밀번호는 영문, 숫자, 특수기호를 포함한 8자 이상이어야 합니다.'
            )
        ]
    )

    confirm_password = PasswordField(
        '새 비밀번호 확인',
        validators=[
            DataRequired(message='새 비밀번호를 다시 입력해주세요.'),
            EqualTo(
                'new_password',
                message='새 비밀번호가 일치하지 않습니다.'
            )
        ]
    )