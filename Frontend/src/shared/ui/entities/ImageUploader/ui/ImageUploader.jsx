import { useState, useRef } from 'react';
import { Paperclip } from 'lucide-react';
import * as classes from './ImageUploader.module.scss';
import UploadModal from './UploadModal';

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const MAX_ASPECT_RATIO = 5; // Максимальное соотношение сторон (например, 5:1 или 1:5)

const ImageUploader = ({ onImageSelect }) => {
    const [error, setError] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const fileInputRef = useRef(null);

    const validateImage = (file) => {
        return new Promise((resolve, reject) => {
            // Проверка типа файла
            if (!file.type.startsWith('image/')) {
                reject('Unsupported image type');
                return;
            }

            // Проверка размера
            if (file.size > MAX_FILE_SIZE) {
                reject('Image size exceeds 10MB limit');
                return;
            }

            // Проверка соотношения сторон
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

    const handleSend = () => {
        if (selectedFile) {
            onImageSelect(selectedFile);
            handleClose();
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