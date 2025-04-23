import React, { useState, useRef } from "react";
import * as classes from "@/shared/ui/entities/InputPassword/ui/InputPassword.module.scss";

// валидный символ = латиница + цифры + спецсимволы
const INVALID_CHAR_REGEX = /[^a-zA-Z0-9!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/;

const InputPassword = () => {
  const [realPassword, setRealPassword] = useState('');
  const [displayPassword, setDisplayPassword] = useState('');
  const [showError, setShowError] = useState(false);
  const timeoutRef = useRef(null);

  const maskPassword = (length) => '•'.repeat(length);

  const revealLastChar = (updatedPassword) => {
    const masked = maskPassword(updatedPassword.length - 1) + updatedPassword.slice(-1);
    setDisplayPassword(masked);
    clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      setDisplayPassword(maskPassword(updatedPassword.length));
    }, 1000);
  };

  const validatePassword = (password) => {
    setShowError(INVALID_CHAR_REGEX.test(password));
  };

  const handleBeforeInput = (e) => {
    const char = e.data;

    if (!char || INVALID_CHAR_REGEX.test(char)) {
      setShowError(true);
      e.preventDefault();
      return;
    }

    const updated = realPassword + char;
    setRealPassword(updated);
    validatePassword(updated);
    revealLastChar(updated);
    e.preventDefault();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Backspace' || e.key === 'Delete') {
      const updated = realPassword.slice(0, -1);
      setRealPassword(updated);
      setDisplayPassword(maskPassword(updated.length));
      validatePassword(updated);
      clearTimeout(timeoutRef.current);
      e.preventDefault();
    }

    if (e.key === ' ') {
      setShowError(true);
      e.preventDefault();
    }
  };

  const handlePaste = (e) => {
    const pasted = e.clipboardData.getData('text');
    const cleaned = pasted.replace(/\s/g, '').replace(INVALID_CHAR_REGEX, '');

    if (!cleaned) {
      setShowError(true);
      return e.preventDefault();
    }

    const updated = realPassword + cleaned.slice(0, 1);
    setRealPassword(updated);
    validatePassword(updated);
    revealLastChar(updated);
    e.preventDefault();
  };

  return (
    <div className={classes.wrapper}>
      <input
        className={classes.form__password}
        type="text"
        autoComplete="off"
        placeholder="Enter your password..."
        value={displayPassword}
        onBeforeInput={handleBeforeInput}
        onKeyDown={handleKeyDown}
        onPaste={handlePaste}
      />
      {showError && (
        <div className={classes.error__message}>
          The password contains an invalid character
        </div>
      )}
    </div>
  );
};

export default InputPassword;
