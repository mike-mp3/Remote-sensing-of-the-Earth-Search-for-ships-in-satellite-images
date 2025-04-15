import * as classes from '@/shared/ui/shared/SubmitButton/ui/SubmitButton.module.scss'


const SubmitButton = ({ children, type = 'button', onClick, disabled }) => {
    return (
      <button  type={type} onClick={onClick} disabled={disabled} className={classes.form__button}>
        {children}
      </button>
    );
  };
  


  export default SubmitButton;