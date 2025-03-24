document.addEventListener('DOMContentLoaded', () => {//тут что-то объявид вроде работает даже
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const imagesContainer = document.querySelector('.images-container');
    let uploadedImages = [];

    // Обработчик события отправки формы
    form.addEventListener('submit', (event) => { //нажатие на кнопку 
        event.preventDefault();

        if (fileInput.files.length > 0) {
            for (let i = 0; i < fileInput.files.length && i < 3; i++) { // Ограничение до трех изображений (не знаю, можно и снять ограничение)
                const reader = new FileReader();
                reader.onload = function(event) {
                    const img = document.createElement('img');
                    img.src = event.target.result;
                    img.classList.add('uploaded-image'); //говорим в какакой класс закинуть 
                    imagesContainer.appendChild(img);
                    uploadedImages.push(img); // Сохраняем ссылку на добавленное изображение
                    console.log(img)
                };
                reader.readAsDataURL(fileInput.files[i]); // Читаем файл
            }
        }
    });
})

document.addEventListener('DOMContentLoaded', function() {
    // Элементы
    const authBtn = document.getElementById('auth-btn');
    const modal = document.getElementById('auth-modal');
    const closeBtn = document.querySelector('.close-btn');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const showLoginBtn = document.getElementById('show-login');
    const showRegisterBtn = document.getElementById('show-register');

    // Открытие модального окна
    authBtn.addEventListener('click', function() {
        modal.style.display = 'block';
        // По умолчанию показываем форму входа
        showLoginForm();
    });

    // Закрытие модального окна
    closeBtn.addEventListener('click', closeModal);
    window.addEventListener('click', function(event) {
        if (event.target === modal) closeModal();
    });

    // Переключение между формами
    showLoginBtn.addEventListener('click', showLoginForm);
    showRegisterBtn.addEventListener('click', showRegisterForm);

    // Обработка формы входа
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Здесь должна быть проверка авторизации
        console.log('Вход:', username, password);
        
        closeModal();
        authBtn.textContent = 'Выйти';
        // Добавьте здесь логику выхода при повторном клике
    });

    // Обработка формы регистрации
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('reg-username').value;
        const password = document.getElementById('reg-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        if (password !== confirmPassword) {
            alert('Пароли не совпадают!');
            return;
        }
        
        // Здесь должна быть логика регистрации
        console.log('Регистрация:', username, password);
        
        alert('Регистрация успешна! Теперь вы можете войти.');
        showLoginForm();
    });

    // Функции
    function closeModal() {
        modal.style.display = 'none';
    }

    function showLoginForm() {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        showLoginBtn.classList.add('active');
        showRegisterBtn.classList.remove('active');
    }

    function showRegisterForm() {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        showLoginBtn.classList.remove('active');
        showRegisterBtn.classList.add('active');
    }
});