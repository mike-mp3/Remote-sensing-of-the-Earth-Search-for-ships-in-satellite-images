import * as classes from "./ModelCard.module.scss";

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
    return (
        <div className={classes.card}>
            <div className={classes.imageContainer}>
                <img src={url} alt="Model preview" className={classes.image} />
                <div className={`${classes.statusOverlay} ${classes[status.toLowerCase()]}`}>
                    {status.toUpperCase()}
                </div>
            </div>
            <div className={classes.footer}>
                <span className={classes.date}>
                    {new Date(created_at).toLocaleDateString()}
                </span>
            </div>
        </div>
    );
};  

export default ModelCard;
