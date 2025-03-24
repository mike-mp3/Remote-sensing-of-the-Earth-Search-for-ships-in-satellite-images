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
    // Получаем элементы
    const authBtn = document.getElementById('auth-btn');
    const modal = document.getElementById('auth-modal');
    const closeBtn = document.querySelector('.close-btn');
    const loginForm = document.getElementById('login-form');

    // Открываем модальное окно при клике на кнопку авторизации
    authBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    // Закрываем модальное окно при клике на крестик
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Закрываем модальное окно при клике вне его
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Обработка формы авторизации
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Здесь можно добавить логику проверки авторизации
        console.log('Логин:', username, 'Пароль:', password);
        
        // Закрываем модальное окно после отправки формы
        modal.style.display = 'none';
        
        // Меняем текст кнопки на "Выйти" после авторизации
        authBtn.textContent = 'Выйти';
        authBtn.addEventListener('click', function() {
            // Логика выхода
            authBtn.textContent = 'Войти';
        });
    });
});