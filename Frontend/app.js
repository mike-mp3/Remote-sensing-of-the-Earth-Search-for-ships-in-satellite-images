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
