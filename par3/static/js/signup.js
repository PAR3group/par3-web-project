document.addEventListener('DOMContentLoaded', function () {
    const agreeAll = document.getElementById('agree_all');
    const children = document.querySelectorAll('.su_agree_child');

    if (!agreeAll) return;

    agreeAll.addEventListener('change', function () {
        children.forEach(function (el) {
            el.checked = agreeAll.checked;
        });
    });

    children.forEach(function (el) {
        el.addEventListener('change', function () {
            agreeAll.checked = Array.from(children).every(function (c) {
                return c.checked;
            });
        });
    });
});