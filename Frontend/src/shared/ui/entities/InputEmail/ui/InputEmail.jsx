import React from "react";
import * as classes from "@/shared/ui/entities/InputEmail/ui/InputEmail.module.scss";



const InputEmail = () => {
    return (
        <input type="email" placeholder="Enter your email..." className={classes.login_form_email}></input>
    )
}



export default InputEmail;