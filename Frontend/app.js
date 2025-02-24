[document.addEventListener](document.addEventListener('DOMContentLoaded'), () => {
    const form = [document.getElementById](document.getElementById('upload-form'));
    const fileInput = [document.getElementById](document.getElementById('file-input'));
    const imagesContainer = [document.querySelector](document.querySelector('.images-container'));
    let uploadedImages = [];

    // Обработчик события отправки формы
    [form.addEventListener](form.addEventListener('submit'), (event) => {
        [event.preventDefault()](event.preventDefault());

        if (fileInput.files.length > 0) {
            for (let i = 0; i < [fileInput.files.length](fileInput.files.length) && i < 3; i++) {
                const reader = new FileReader();
                [reader.onload](reader.onload) = function(event) {
                    const img = [document.createElement](document.createElement('img'));
                    [img.src](img.src) = [event.target.result](event.target.result);
                    [img.classList.add](img.classList.add('uploaded-image'));
                    [imagesContainer.appendChild(img)](imagesContainer.appendChild(img));
                    [uploadedImages.push(img)](uploadedImages.push(img));
                };
                [reader.readAsDataURLfileInput.files](reader.readAsDataURL(fileInput.files)[i]);
            }
        }
    });
});