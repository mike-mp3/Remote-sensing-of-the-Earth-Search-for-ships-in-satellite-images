import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import LoginSchema from "@/shared/lib/validation/LoginShema";
import * as classes from "@/shared/ui/widgets/LoginForm/ui/LoginForm.module.scss";

const LoginForm = () => {
  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      const response = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });

      const result = await response.json();

      if (response.ok) {
        console.log("успешный вход епта бля:", result);

        resetForm();
      } else {
        console.error("ошибка авторизации пошел ты сученок:", result.message);
      }
    } catch (err) {
      console.error("ошибка сети пососи:", err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Formik
      initialValues={{ email: "", password: "" }}
      validationSchema={LoginSchema}
      onSubmit={handleSubmit}
    >
      {({ isSubmitting }) => (
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
              placeholder="Enter your password..."
              className={classes.form__input}
            />
            <div className={classes.form__errors}>
              <ErrorMessage name="email" component="div" className={classes.error__message} />
              <ErrorMessage name="password" component="div" className={classes.error__message} />
            </div>
            <button
              type="submit"
              className={classes.form__button}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Loading..." : "Log in"}
            </button>
          </div>
        </Form>
      )}
    </Formik>
  );
};

export default LoginForm;
