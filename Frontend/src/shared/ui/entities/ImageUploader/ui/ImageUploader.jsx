import { useState, useRef } from 'react';
import { Paperclip } from 'lucide-react';
import * as classes from './ImageUploader.module.scss';
import UploadModal from './UploadModal';

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const MAX_ASPECT_RATIO = 5;
const API_URL = import.meta.env.VITE_API_BASE_URL;


const ImageUploader = ({ onImageSelect, onUploadStart }) => {
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  // Проверка типа, размера и соотношения сторон
  const validateImage = (file) =>
    new Promise((resolve, reject) => {
      if (!file.type.startsWith('image/')) return reject('Unsupported image type');
      if (file.size > MAX_FILE_SIZE) return reject('Image size exceeds 10 MB');

      const img = new Image();
      img.onload = () => {
        const ratio = img.width / img.height;
        if (ratio > MAX_ASPECT_RATIO || ratio < 1 / MAX_ASPECT_RATIO) {
          reject('Unsupported image aspect ratio');
        } else {
          resolve(file);
        }
      };
      img.onerror = () => reject('Failed to load image');
      img.src = URL.createObjectURL(file);
    });

  // При выборе файла в проводнике
  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setError(null);
    try {
      const valid = await validateImage(file);
      setSelectedFile(valid);
    } catch (err) {
      setError(err);
      console.error('Validation error:', err);
    }
  };

  // Программный клик по скрытому инпуту
  const handleClick = () => {
    fileInputRef.current?.click();
  };

  // Сброс выбранного файла
  const handleClose = () => {
    setSelectedFile(null);
    fileInputRef.current.value = '';
  };

  // Отправка файла на сервер
  const handleSend = async () => {
    if (!selectedFile) return;

    onUploadStart?.();

    try {
      // 1) Получаем presigned POST данные
      const presignedRes = await fetch(`${API_URL}/core/prompt/s3/presigned-post`, {
        method: 'POST',
        credentials: 'include',
      });
      if (!presignedRes.ok) throw new Error('Failed to get presigned data');
      const { fields } = await presignedRes.json();

      // 2) Загружаем на S3
      const formData = new FormData();
      Object.entries(fields).forEach(([k, v]) => formData.append(k, v));
      formData.append('file', selectedFile);
      const uploadRes = await fetch(`${API_URL}/s3/user-prompts`, {
        method: 'POST',
        body: formData,
      });
      if (!uploadRes.ok) throw new Error('Failed to upload to S3');

      // 3) Уведомляем backend, что можно начинать обработку
      const notifyRes = await fetch(`${API_URL}/core/prompt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key_path: fields.key }),
        credentials: 'include',
      });
      if (!notifyRes.ok) throw new Error('Failed to notify backend');
      const { id, prompt_id } = await notifyRes.json();
      
      // 4) Прокидываем новый prompt наверх с минимальным набором полей
      onImageSelect({
        id,
        prompt_id: prompt_id,
        status: 'pending',
        url: URL.createObjectURL(selectedFile), // временный превью
        created_at: new Date().toISOString(),
        raw_key: fields.key,
      });

      // 5) Закрываем модалку
      handleClose();
    } catch (err) {
      setError(err.message);
      console.error('Upload error:', err);
    }
  };

  return (
    <>
      <div className={classes.uploader}>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept="image/*"
          className={classes.hiddenInput}
        />
        <button
          className={classes.uploadButton}
          onClick={handleClick}
          disabled={!!selectedFile}
          title="Upload image"
        >
          <Paperclip size={24} />
        </button>
        {error && <div className={classes.error}>{error}</div>}
      </div>

      {selectedFile && (
        <UploadModal
          fileName={selectedFile.name}
          onClose={handleClose}
          onSend={handleSend}
        />
      )}
    </>
  );
};

export default ImageUploader;
