import React, { useState } from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import * as classes from "@/shared/ui/widgets/LoginForm/ui/LoginForm.module.scss";
import { Link, useNavigate } from "react-router-dom";

const RegistrationForm = () => {
  const navigate = useNavigate();
  const [serverError, setServerError] = useState("");

  const initialValues = {
    email: "",
    password: "",
  };

  const validationSchema = Yup.object({
    email: Yup.string()
      .email("invalid email")
      .required("Email is empty"),
    password: Yup.string()
      .min(8, "Invalid (min 8 chars and 1 digit)")
      .matches(/\d/, "min 1 digit")
      .required("Password is emty"),
  });

  const handleSubmit = async (values, { setSubmitting }) => {
    setServerError(""); 

    try {
      const response = await fetch("https://fd5c-89-191-234-252.ngrok-free.app/core/user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(values),
      });

      if (response.status === 201) {
        navigate("/confirm", { state: { email: values.email } });
      } else if (response.status === 409) {
        const data = await response.json();
        setServerError(data.detail?.[0] || "User already exists");

      } else if (response.status === 422) {
        const data = await response.json();
        const messages = data.detail?.map((err) => err.msg).join(", ");
        setServerError(messages || "Validation error");

      } else {
        console.error("Unhandled error", data);
      }

    } catch (error) {
      console.error("Registration error:", error);
      setServerError("Network or server error");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      {({ errors, touched, isSubmitting }) => (
        <Form className={classes.form__container}>
          <div className={classes.form__content}>
            <Field
              type="email"
              name="email"
              placeholder="Enter your email..."
              className={classes.form__input}
            />
            <Field
              type="password"
              name="password"
              placeholder="Create your password..."
              className={classes.form__input}
            />

            {(errors.email && touched.email) || (errors.password && touched.password) ? (
              <div className={classes.form__errors}>
                {errors.email && touched.email && (
                  <div className={classes.error__message}>{errors.email}</div>
                )}
                {errors.password && touched.password && (
                  <div className={classes.error__message}>{errors.password}</div>
                )}
              </div>
            ) : null}

            {/* Отображение ошибки от сервера, если есть */}
            {serverError && (
              <div className={classes.form__errors}>
                <div className={classes.error__message}>{serverError}</div>
              </div>
            )}

            <button
              type="submit"
              className={classes.form__button}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Loading..." : "Sign up"}
            </button>
            <div className={classes.form__link}>
              Have an account? <Link to="/">Log in</Link>
            </div>
          </div>
        </Form>
      )}
    </Formik>
  );
};

export default RegistrationForm;
