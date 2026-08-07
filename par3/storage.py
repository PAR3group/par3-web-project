import uuid

import requests

import config


class StorageUploadError(RuntimeError):
    pass


def upload_image(file_storage, folder):
    """업로드된 파일을 Supabase Storage에 저장하고 공개 URL을 반환한다.

    file_storage: Flask request.files에서 받은 FileStorage 객체
    folder: 버킷 안에서 파일을 묶어둘 폴더명 (예: 'avatars', 'talk', 'shop')
    """
    if not config.SUPABASE_URL or not config.SUPABASE_SERVICE_ROLE_KEY:
        raise StorageUploadError(
            'SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY 환경변수가 설정되어 있지 않습니다.'
        )

    filename = file_storage.filename or ''
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'bin'
    object_path = f"{folder}/{uuid.uuid4().hex}.{ext}"

    response = requests.post(
        f"{config.SUPABASE_URL}/storage/v1/object/{config.SUPABASE_STORAGE_BUCKET}/{object_path}",
        headers={
            'apikey': config.SUPABASE_SERVICE_ROLE_KEY,
            'Authorization': f'Bearer {config.SUPABASE_SERVICE_ROLE_KEY}',
            'Content-Type': file_storage.content_type or 'application/octet-stream',
        },
        data=file_storage.read(),
    )

    if response.status_code >= 300:
        raise StorageUploadError(f'Supabase Storage 업로드 실패: {response.status_code} {response.text}')

    return f"{config.SUPABASE_URL}/storage/v1/object/public/{config.SUPABASE_STORAGE_BUCKET}/{object_path}"