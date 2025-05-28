import * as classes from "./ModelCard.module.scss";
import { ThreeDots } from 'react-loader-spinner';
const ModelCard = ({ 
    id,
    user_id,
    prompt_id,
    raw_key,
    result_key,
    status,
    created_at,
    updated_at,
    url 
}) => {
    // Форматирование даты и времени
    const formatDateTime = (dateString) => {
        const date = new Date(dateString);
        return {
            date: date.toLocaleDateString('ru-RU'), // Формат ДД.ММ.ГГГГ
            time: date.toLocaleTimeString('ru-RU', { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: false // 24-часовой формат
            })
        };
    };

    const { date, time } = formatDateTime(created_at);

    return (
        <div className={classes.card}>
            <div className={classes.imageContainer}>
                <img src={url} alt="Model preview" className={classes.image} />
                
                {status.toLowerCase() === 'pending' && (
                    <div className={classes.loaderOverlay}>
                        <ThreeDots
                            key={`loader-${status}`}
                            visible={true}
                            height="80"
                            width="80"
                            color="#1e509f" 
                            radius="9"
                            ariaLabel="three-dots-loading"
                        />
                    </div>
                )}
                
                {status.toLowerCase() === 'error' && (
                    <div className={`${classes.statusOverlay} ${classes[status.toLowerCase()]}`}>
                        {status.toUpperCase()}
                    </div>
                )}
            </div>
            <div className={classes.footer}>
                <span className={classes.date}>{date}</span>
                <span className={classes.time}>{time}</span>
            </div>
        </div>
    );
};
export default ModelCard;