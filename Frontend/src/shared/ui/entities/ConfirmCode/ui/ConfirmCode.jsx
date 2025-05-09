import React, { useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import * as classes from "@/shared/ui/entities/ConfirmCode/ui/ConfirmCode.module.scss";

const ConfirmCode = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const email = location.state?.email || "example@gmail.com";

  const inputCount = 6;
  const [values, setValues] = useState(Array(inputCount).fill(""));
  const [errorMessage, setErrorMessage] = useState("");
  const inputsRef = useRef([]);

  const handleChange = (index, event) => {
    const value = event.target.value;

    if (!/^\d?$/.test(value)) return;

    const newValues = [...values];
    newValues[index] = value;
    setValues(newValues);

    if (value && index < inputCount - 1) {
      if (inputsRef.current[index + 1]) {
        inputsRef.current[index + 1].focus();
      }
    }

    if (newValues.every((val) => val !== "")) {
      const code = newValues.join("");
      submitCode(code);
    }
  };

  const handleKeyDown = (index, event) => {
    if (event.key === "Backspace") {
      if (values[index] === "") {
        if (index > 0 && inputsRef.current[index - 1]) {
          inputsRef.current[index - 1].focus();
        }
      } else {
        const newValues = [...values];
        newValues[index] = "";
        setValues(newValues);
      }
    }
  };

  const submitCode = async (code) => {
    console.log("Sending verification code:", code, "email:", email);

    try {
      const response = await fetch("http://localhost:8500/user/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          confirmation_code: code,
        }),
      });

      if (response.status === 200) {
        const data = await response.json();
        console.log("Code verified successfully:", data);
        navigate("/home");
      } else if (response.status === 400 || response.status === 404) {
        const errorData = await response.json();
        setErrorMessage(errorData.detail?.[0] || "Произошла ошибка.");
      } else if (response.status === 422) {
        const errorData = await response.json();
        setErrorMessage("Error validation: " + JSON.stringify(errorData.detail));
      } else {
        setErrorMessage(`Undefined error: ${response.status}`);
      }
    } catch (error) {
      setErrorMessage("Network error. Try again later");
      console.error("Network or unexpected error:", error);
    }
  };

  return (
    <div className={classes.verification_wrapper}>
      <div className={classes.verification_content}>
        <h1 className={classes.verification_content_text}>
          The code has been sent to your email<br />Enter your code
        </h1>

        <div className={classes.verification_input}>
          {values.map((val, idx) => (
            <input
              key={idx}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={val}
              onChange={(e) => handleChange(idx, e)}
              onKeyDown={(e) => handleKeyDown(idx, e)}
              ref={(el) => (inputsRef.current[idx] = el)}
              className={classes.verification_input__cell}
            />
          ))}
        </div>

        {errorMessage && (
          <div className={classes.error__message}>
            {errorMessage}
          </div>
        )}
      </div>
    </div>
  );
};

export default ConfirmCode;
