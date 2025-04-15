import React from "react";
import { InputEmail } from "@/shared/ui/entities/InputEmail";
import { InputPassword } from "@/shared/ui/entities/InputPassword";
import { SubmitButton } from "@/shared/ui/shared/SubmitButton";
import * as classes from "@/shared/ui/widgets/LoginForm/ui/LoginForm.module.scss"



const LoginForm = () =>{
    return(
        <form className={classes.form__container}>
        <div className={classes.form__content}>
          <InputEmail className={classes.form__input} />
          <InputPassword className={classes.form__input} />
          <SubmitButton className={classes.form__button}>
            Log in
          </SubmitButton>
        </div>
      </form>
    )
}


export default LoginForm;















