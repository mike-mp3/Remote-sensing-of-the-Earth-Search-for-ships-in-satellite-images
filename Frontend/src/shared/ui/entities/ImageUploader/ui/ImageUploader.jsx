import { useState, useRef } from 'react';
import { Paperclip } from 'lucide-react';
import * as classes from './ImageUploader.module.scss';
import UploadModal from './UploadModal';

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const MAX_ASPECT_RATIO = 5; 

const URL = import.meta.env.VITE_API_BASE_URL;

const ImageUploader = ({ onImageSelect, onUploadStart }) => {
    const [error, setError] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const fileInputRef = useRef(null);

    const validateImage = (file) => {
        return new Promise((resolve, reject) => {
            if (!file.type.startsWith('image/')) {
                reject('Unsupported image type');
                return;
            }

            if (file.size > MAX_FILE_SIZE) {
                reject('Image size exceeds 10MB limit');
                return;
            }

            const img = new Image();
            img.onload = () => {
                const aspectRatio = img.width / img.height;
                if (aspectRatio > MAX_ASPECT_RATIO || aspectRatio < 1 / MAX_ASPECT_RATIO) {
                    reject('Unsupported image aspect ratio');
                } else {
                    resolve(file);
                }
            };
            img.onerror = () => {
                reject('Failed to load image');
            };
            img.src = URL.createObjectURL(file);
        });
    };

    const handleFileSelect = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setError(null);
        try {
            const validatedFile = await validateImage(file);
            setSelectedFile(validatedFile);
        } catch (err) {
            setError(err);
            console.error('Image validation error:', err);
        }
    };

    const handleClick = () => {
        if (!selectedFile) {
            fileInputRef.current?.click();
        }
    };

    const handleClose = () => {
        setSelectedFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const handleSend = async () => {
        if (!selectedFile) return;

        try {
            // Сообщаем родителю о начале загрузки
            if (typeof onUploadStart === 'function') {
                onUploadStart();
            }

            // 1. Получаем presigned POST данные
            const presignedRes = await fetch(`${URL}/core/prompt/s3/presigned-post`, {
                method: "POST",
                credentials: "include"
            });

            if (!presignedRes.ok) {
                throw new Error("Failed to get presigned POST data");
            }

            const presignedData = await presignedRes.json();
            const { url, fields } = presignedData;
            // 2. Собираем форму
            const formData = new FormData();
            Object.entries(fields).forEach(([key, value]) => {
                formData.append(key, value);
            });
            formData.append("file", selectedFile);

            // 3. Загружаем на S3
            const uploadRes = await fetch(`${URL}/s3/user-prompts`, {
                method: "POST",
                body: formData
            });

            if (!uploadRes.ok) {
                throw new Error("Failed to upload image to S3");
            }
            console.log("presignedData.key", presignedData.fields.key);
            const notifyRes = await fetch(`${URL}/core/prompt`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({"key_path": presignedData.fields.key}),
                credentials: "include"
            });
// dkkdfmkdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
            if (!notifyRes.ok) {
                throw new Error("Failed to notify backend");
            }

            console.log("Image uploaded and backend notified successfully.");

            // Уведомляем родителя, если нужно продолжать
            if (typeof onImageSelect === 'function') {
                onImageSelect(selectedFile);
            }

            handleClose();
        } catch (err) {
            setError(err.message);
            console.error("Upload error:", err);
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
                    title="Upload image"
                    disabled={!!selectedFile}
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
