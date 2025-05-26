import * as Yup from "yup";

const LoginSchema = Yup.object().shape({
  email: Yup.string()
    .email("Некорректный email")
    .required("Email обязателен"),

  password: Yup.string()
    .min(8, "Минимум 8 символов")
    .matches(/\d/, "Пароль должен содержать хотя бы одну цифру")
    .required("Пароль обязателен"),
});


export default LoginSchema