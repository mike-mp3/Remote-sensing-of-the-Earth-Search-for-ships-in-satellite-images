import React from "react";
import { InputEmail } from "@/shared/ui/entities/InputEmail";
import { InputPassword } from "@/shared/ui/entities/InputPassword";
import * as classes from "@/shared/ui/widgets/LoginForm/ui/LoginForm.module.scss"



const LoginForm = () =>{
    return(
        <form className={classes.form_container_}>
            <InputEmail/>
            <InputPassword/>
        </form>
    )
}


export default LoginForm;
