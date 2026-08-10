// shop_admin_form.js
// 상품 등록/수정 폼의 "상세 설명" 블록(텍스트/이미지)을 순서대로 추가·삭제하는 공통 스크립트.
// 수정 폼에서는 #existingBlocksData(JSON) 내용을 읽어 기존 블록을 미리 채워둔다.
(function () {
    const container = document.getElementById('detailBlocks');
    if (!container) return;

    const addTextBt = document.getElementById('addTextBlockBt');
    const addImageBt = document.getElementById('addImageBlockBt');
    let seq = 0;

    function makeHead(labelText, onRemove) {
        const head = document.createElement('div');
        head.className = 'sa_detail_block_head';

        const label = document.createElement('span');
        label.className = 'sa_detail_block_label';
        label.textContent = labelText;

        const removeBt = document.createElement('button');
        removeBt.type = 'button';
        removeBt.className = 'sa_block_remove_bt';
        removeBt.textContent = '삭제';
        removeBt.addEventListener('click', onRemove);

        head.appendChild(label);
        head.appendChild(removeBt);
        return head;
    }

    function addTextBlock(existingText) {
        const i = seq++;
        const row = document.createElement('div');
        row.className = 'sa_detail_block';

        row.appendChild(makeHead('텍스트', () => row.remove()));

        const typeInput = document.createElement('input');
        typeInput.type = 'hidden';
        typeInput.name = `detail_type_${i}`;
        typeInput.value = 'text';

        const textarea = document.createElement('textarea');
        textarea.className = 'sa_form_input sa_detail_textarea';
        textarea.name = `detail_text_${i}`;
        textarea.placeholder = '설명 텍스트를 입력하세요';
        textarea.value = existingText || '';

        row.appendChild(typeInput);
        row.appendChild(textarea);
        container.appendChild(row);
    }

    function addImageBlock(existingUrl) {
        const i = seq++;
        const row = document.createElement('div');
        row.className = 'sa_detail_block';

        row.appendChild(makeHead('이미지', () => row.remove()));

        const typeInput = document.createElement('input');
        typeInput.type = 'hidden';
        typeInput.name = `detail_type_${i}`;
        typeInput.value = 'image';
        row.appendChild(typeInput);

        if (existingUrl) {
            const img = document.createElement('img');
            img.className = 'sa_detail_existing_img';
            img.src = existingUrl;
            img.alt = '기존 이미지';
            row.appendChild(img);

            const existingInput = document.createElement('input');
            existingInput.type = 'hidden';
            existingInput.name = `detail_existing_image_${i}`;
            existingInput.value = existingUrl;
            row.appendChild(existingInput);

            const hint = document.createElement('p');
            hint.className = 'sa_detail_hint';
            hint.textContent = '새 이미지를 선택하면 기존 이미지가 교체됩니다.';
            row.appendChild(hint);
        }

        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.className = 'sa_form_input';
        fileInput.name = `detail_image_${i}`;
        fileInput.accept = 'image/*';
        row.appendChild(fileInput);

        container.appendChild(row);
    }

    if (addTextBt) addTextBt.addEventListener('click', () => addTextBlock());
    if (addImageBt) addImageBt.addEventListener('click', () => addImageBlock());

    const dataEl = document.getElementById('existingBlocksData');
    if (dataEl) {
        try {
            const existing = JSON.parse(dataEl.textContent || '[]');
            existing.forEach((b) => {
                if (b.type === 'text') addTextBlock(b.text);
                else if (b.type === 'image') addImageBlock(b.image);
            });
        } catch (e) {
            console.error('상세설명 블록 로드 실패', e);
        }
    }
})();
