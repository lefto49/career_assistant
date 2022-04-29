import React from "react";
import { NavLink } from "react-router-dom";
import "./../style.css";

const Login = (props) => {
  return (
    <form
      className="form"
      action="#"
      onSubmit={(e) => {
        props.handleFormSubmit(e);
      }}
    >
      <h1>Login</h1>
      <div className="input-form">
        <input
          type="text"
          required
          placeholder="Email"
          autoComplete="off"
          value={props.propperty.email}
          onChange={(e) => {
            props.setPropperty({ ...props.propperty, email: e.target.value });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="password"
          required
          autoComplete="off"
          placeholder="Password"
          value={props.propperty.password}
          onChange={(e) => {
            props.setPropperty({
              ...props.propperty,
              password: e.target.value,
            });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="submit"
          value="Enter"
          onClick={(e) => {
            e.preventDefault();
            props.submitForm();
          }}
        />
      </div>
      <NavLink to="/forgotPassword">Забыли пароль?</NavLink>
      <NavLink to="/registration">Регистрация</NavLink>
    </form>
  );
};

export default Login;
