import React from 'react'
import { NavLink } from 'react-router-dom';
import "./../style.css";

const Login = () => {
  return (
    <form className ="form">
      <h1>Login</h1>
      <div className ="input-form">
        <input type="text" placeholder="Email"/>
      </div>
      <div className ="input-form">
        <input type="password" placeholder="Password"/>
      </div>
      <div className="input-form">
        <input type="submit" value="Enter"/>
      </div>
      <NavLink to="">Забыли пароль?</NavLink>
      <NavLink to="">Регистрация</NavLink>
    </form>
  )
}

export default Login;