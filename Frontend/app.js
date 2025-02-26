document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const imagesContainer = document.querySelector('.images-container');
    let uploadedImages = [];

    // Обработчик события отправки формы
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        if (fileInput.files.length > 0) {
            for (let i = 0; i < fileInput.files.length && i < 3; i++) { // Ограничение до трех изображений
                const reader = new FileReader();
                reader.onload = function(event) {
                    const img = document.createElement('img');
                    img.src = event.target.result;
                    img.classList.add('uploaded-image');
                    imagesContainer.appendChild(img);
                    uploadedImages.push(img); // Сохраняем ссылку на добавленное изображение
                };
                reader.readAsDataURL(fileInput.files[i]); // Читаем файл
            }
        }
    });
})