import React from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Link } from "react-router-dom";
import * as classes from "@/shared/ui/widgets/LoginForm/ui/LoginForm.module.scss";

const RegistrationForm = () => {
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

  const handleSubmit = (values, { setSubmitting }) => {
    console.log("sending data to the server:", values);
    setTimeout(() => {
      setSubmitting(false);
    }, 1000);
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

            {/* рендеринг блока ошибок */}

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
