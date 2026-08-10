// ======================================================
// TALK 상세페이지 JavaScript
// 좋아요 / 댓글 등록
// ======================================================


/* ======================================================
   1. 좋아요
   ====================================================== */

async function likePost(postId) {

    try {

        const response = await fetch(`/talk/${postId}/like`, {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            }
        });


        // 서버에서 받은 데이터
        const data = await response.json();


        // ------------------------------------------
        // 로그인이 안 되어 있는 경우
        // ------------------------------------------
        if (response.status === 401 || data.need_login) {

            alert('로그인이 필요한 기능입니다.');

            return;
        }


        // ------------------------------------------
        // 좋아요 처리 실패
        // ------------------------------------------
        if (!response.ok || !data.success) {

            alert(
                data.message ||
                '좋아요 처리 중 오류가 발생했습니다.'
            );

            return;
        }


        // ------------------------------------------
        // 좋아요 숫자 화면에 바로 반영
        // ------------------------------------------
        const likeCount =
            document.getElementById('like-count');

        if (likeCount) {

            likeCount.textContent = data.likes;

        }


        // 좋아요 버튼 활성화 표시
        const likeButton =
            document.getElementById('like-btn');

        if (likeButton) {

            likeButton.classList.add('active');

        }


    } catch (error) {

        console.error(
            '좋아요 오류:',
            error
        );

        alert(
            '좋아요 처리 중 오류가 발생했습니다.'
        );

    }

}



/* ======================================================
   2. 댓글 등록
   ====================================================== */

async function addComment(postId) {

    const commentInput =
        document.getElementById('comment-input');


    // input 자체를 찾지 못했을 경우
    if (!commentInput) {

        console.error(
            'comment-input을 찾을 수 없습니다.'
        );

        return;
    }


    // 작성된 댓글 가져오기
    const content =
        commentInput.value.trim();


    // ------------------------------------------
    // 댓글을 입력하지 않은 경우
    // ------------------------------------------
    if (!content) {

        alert(
            '댓글 내용을 입력해 주세요.'
        );

        commentInput.focus();

        return;
    }


    try {

        const response = await fetch(
            `/talk/${postId}/comment`,
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify({
                    content: content
                })
            }
        );


        // 서버에서 받은 데이터
        const data =
            await response.json();


        // ------------------------------------------
        // 로그인이 안 되어 있을 경우
        // ------------------------------------------
        if (
            response.status === 401 ||
            data.need_login
        ) {

            alert(
                '로그인이 필요한 기능입니다.'
            );

            return;
        }


        // ------------------------------------------
        // 댓글 등록 실패
        // ------------------------------------------
        if (
            !response.ok ||
            !data.success
        ) {

            alert(
                data.message ||
                '댓글 등록 중 오류가 발생했습니다.'
            );

            return;
        }


        // ------------------------------------------
        // 등록 성공
        // ------------------------------------------

        // 입력창 비우기
        commentInput.value = '';


        /*
            댓글은 DB에 이미 저장된 상태입니다.

            상세페이지를 다시 불러오면
            Flask가 새 댓글을 포함한
            post.comments_list를 다시 가져옵니다.
        */
        window.location.reload();


    } catch (error) {

        console.error(
            '댓글 등록 오류:',
            error
        );

        alert(
            '댓글 등록 중 오류가 발생했습니다.'
        );

    }

}



/* ======================================================
   3. 댓글 입력창 Enter 처리
   ====================================================== */

/*
   HTML의 onkeydown에서도 Enter 처리가 되어 있기 때문에
   현재는 별도의 이벤트 코드를 추가하지 않습니다.
*/