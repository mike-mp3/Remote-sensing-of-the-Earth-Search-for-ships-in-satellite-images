import { useState, useRef } from 'react';
import { Paperclip } from 'lucide-react';
import * as classes from './ImageUploader.module.scss';
import UploadModal from './UploadModal';
import WebSocketListener from './WebSocketListener'; // 💡 Новый компонент

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const MAX_ASPECT_RATIO = 5;
const URLL = import.meta.env.VITE_API_BASE_URL;

const ImageUploader = ({ onImageSelect, onUploadStart, onProcessingDone }) => {
    const [error, setError] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [wsActive, setWsActive] = useState(false); // флаг активности WebSocket

    const fileInputRef = useRef(null);

    const validateImage = (file) => {
        return new Promise((resolve, reject) => {
            if (!file.type.startsWith('image/')) return reject('Unsupported image type');
            if (file.size > MAX_FILE_SIZE) return reject('Image size exceeds 10MB limit');

            const img = new Image();
            img.onload = () => {
                const aspectRatio = img.width / img.height;
                if (aspectRatio > MAX_ASPECT_RATIO || aspectRatio < 1 / MAX_ASPECT_RATIO) {
                    reject('Unsupported image aspect ratio');
                } else {
                    resolve(file);
                }
            };
            img.onerror = () => reject('Failed to load image');
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
        fileInputRef.current.value = '';
    };

    const handleSend = async () => {
        if (!selectedFile) return;

        try {
            if (typeof onUploadStart === 'function') {
                onUploadStart();
            }

            const presignedRes = await fetch(`${URLL}/core/prompt/s3/presigned-post`, {
                method: "POST",
                credentials: "include"
            });

            if (!presignedRes.ok) throw new Error("Failed to get presigned POST data");

            const presignedData = await presignedRes.json();
            const { url, fields } = presignedData;

            const formData = new FormData();
            Object.entries(fields).forEach(([key, value]) => formData.append(key, value));
            formData.append("file", selectedFile);

            const uploadRes = await fetch(`${URLL}/s3/user-prompts`, {
                method: "POST",
                body: formData
            });

            if (!uploadRes.ok) throw new Error("Failed to upload image to S3");

            const notifyRes = await fetch(`${URLL}/core/prompt`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "key_path": presignedData.fields.key }),
                credentials: "include"
            });

            if (!notifyRes.ok) throw new Error("Failed to notify backend");

            // запускаем WebSocket после успешной отправки
            setWsActive(true);
        } catch (err) {
            setError(err.message);
            console.error("Upload error:", err);
        }
    };

    const handleProcessingDone = () => {
        setWsActive(false);
        handleClose();
        if (typeof onImageSelect === 'function') {
            onImageSelect(selectedFile);
        }
        if (typeof onProcessingDone === 'function') {
            onProcessingDone();
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
            {wsActive && (
                <WebSocketListener
                    url={`ws://fd5c-89-191-234-252.ngrok-free.app/notifier/prompt/result`} // пример URL
                      onClose={handleProcessingDone}
                />
            )}
        </>
    );
};

export default ImageUploader;
