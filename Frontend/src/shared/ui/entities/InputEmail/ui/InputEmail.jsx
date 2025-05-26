import React, { useState } from "react";
import * as classes from "@/shared/ui/entities/InputEmail/ui/InputEmail.module.scss";

// Простой email regex (подойдёт для большинства задач)
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const InputEmail = () => {
  const [email, setEmail] = useState('');
  const [showError, setShowError] = useState(false);

  const handleChange = (e) => {
    const value = e.target.value;

    // запрещаем пробелы вообще
    if (value.includes(' ')) return;

    setEmail(value);

    // проверка: если поле не пустое и не проходит regex — ошибка
    if (value && !EMAIL_REGEX.test(value)) {
      setShowError(true);
    } else {
      setShowError(false);
    }
  };

  return (
    <div className={classes.wrapper}>
      <input
        type="email"
        placeholder="Enter your email..."
        className={classes.form__email}
        value={email}
        onChange={handleChange}
        autoComplete="off"
      />
      {showError && (
        <div className={classes.error__message}>
          Please enter a valid email
        </div>
      )}
    </div>
  );
};

export default InputEmail;
