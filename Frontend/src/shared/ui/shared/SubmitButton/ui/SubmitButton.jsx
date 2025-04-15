import * as classes from '@/shared/ui/shared/SubmitButton/ui/SubmitButton'


const SubmitButton = ({ children, type = 'button', onClick, disabled }) => {
    return (
      <button className={classes.form_container_button} type={type} onClick={onClick} disabled={disabled}>
        {children}
      </button>
    );
  };
  


  export default SubmitButton;