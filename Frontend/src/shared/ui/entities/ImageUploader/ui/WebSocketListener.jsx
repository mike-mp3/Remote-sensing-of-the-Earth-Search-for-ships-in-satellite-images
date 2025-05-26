import { useEffect } from 'react';

const WebSocketListener = ({ url, onClose }) => {
    useEffect(() => {
        const ws = new WebSocket(url);

        ws.onopen = () => {
            console.log('WebSocket открыт:', url);
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('📨 Получено сообщение:', data);
        };

        ws.onerror = (error) => {
            console.error(' WebSocket ошибка:', error);
        };

        ws.onclose = () => {
            console.log(' WebSocket закрыт');
            if (typeof onClose === 'function') {
                onClose(); // сообщаем родителю
            }
        };

        return () => {
            console.log(' WebSocket закрытие вручную');
            ws.close();
        };
    }, [url, onClose]);

    return null;
};

export default WebSocketListener;
