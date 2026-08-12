const passwordModal = document.getElementById('password-modal');
const openPasswordBtn = document.getElementById('btn-open-password');
const closePasswordBtn = document.getElementById('btn-close-password');

if (openPasswordBtn && passwordModal) {
    openPasswordBtn.addEventListener('click', function () {
        passwordModal.classList.add('show');
    });
}

if (closePasswordBtn && passwordModal) {
    closePasswordBtn.addEventListener('click', function () {
        passwordModal.classList.remove('show');
    });
}

if (passwordModal) {
    passwordModal.addEventListener('click', function (e) {
        if (e.target === passwordModal) {
            passwordModal.classList.remove('show');
        }
    });
}