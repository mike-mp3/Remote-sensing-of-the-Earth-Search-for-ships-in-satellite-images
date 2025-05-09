import { X } from 'lucide-react';
import * as classes from './UploadModal.module.scss';

const UploadModal = ({ fileName, onClose, onSend }) => {
    return (
        <div className={classes.modalOverlay}>
            <div className={classes.modal}>
                <button className={classes.closeButton} onClick={onClose}>
                    <X size={24} />
                </button>
                <div className={classes.content}>
                    <h3 className={classes.title}>Upload Image</h3>
                    <p className={classes.fileName}>{fileName}</p>
                    <button className={classes.sendButton} onClick={onSend}>
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default UploadModal; 