function checkSearch(form) {
            // 공백만 입력했거나 아무것도 입력 안 했을 때 검사
            if (!form.keyword.value.trim()) {
                alert('검색어를 입력해 주세요');
                form.keyword.focus();
                return false; // 폼 제출 중단
            }
            return true; // 정상 제출
        }