import React from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Link, useNavigate } from "react-router-dom";
import * as classes from "@/shared/ui/widgets/LoginForm/ui/LoginForm.module.scss";
import { useUser } from "@/shared/lib/context/UserContext";

const LoginForm = () => {
  const navigate = useNavigate();
  const { updateUserEmail } = useUser();
  
  const initialValues = {
    email: "",
    password: "",
  };

  const validationSchema = Yup.object({
    email: Yup.string()
      .email("Invalid email")
      .required("Email is empty"),
    password: Yup.string()
      .min(8, "Invalid (min 8 chars and 1 digit)")
      .matches(/\d/, "min 1 digit")
      .required("Password is emty"),
  });

  const handleSubmit = async (values, { setSubmitting, setErrors }) => {
    try {
      const response = await fetch("https://fd5c-89-191-234-252.ngrok-free.app/core/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: include,
        body: JSON.stringify(values),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        console.log("Successful authorization:", data);
        updateUserEmail(values.email);
        navigate("/home");
      } else if (response.status === 403) {
        setErrors({ password: "User not verified" });
      } else if (response.status === 404) {
        setErrors({ email: "Incorrect email or password", password: " " });
      } else if (response.status === 422) {
        setErrors({ email: "Data validation error" });
      } else {
        console.error("Unhandled error", data);
      }
    } catch (error) {
      console.error("Error sending request:", error);
      setErrors({ email: "Network or server error" });
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
              placeholder="Enter your password..."
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

            <button
              type="submit"
              className={classes.form__button}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Loading..." : "Log in"}
            </button>

            <div className={classes.form__link}>
              Don't have an account? <Link to="/signup">Sign up</Link>
            </div>
          </div>
        </Form>
      )}
    </Formik>
  );
};

export default LoginForm;
