import React from 'react'
import { NavLink } from 'react-router-dom';
import "./../style.css";

const Login = (props) => {
  return (
    <form className ="form">
      <h1>Login</h1>
      <div className ="input-form">
        <input type="text" placeholder="Email" value={props.propperty.email} onChange ={(e)=>{
          props.setPropperty({...props.propperty,email: e.target.value});
        }}/>
      </div>
      <div className ="input-form">
        <input type="password" placeholder="Password" value={props.propperty.password} onChange ={(e)=>{
          props.setPropperty({...props.propperty,password: e.target.value});
        }}/>
      </div>
      <div className="input-form">
        <input type="submit" value="Enter" onClick={(e)=>{
          e.preventDefault(); 
          props.submitForm();
        }}/>
      </div>
      <NavLink to="">Забыли пароль?</NavLink>
      <NavLink to="">Регистрация</NavLink>
    </form>
  )
}

export default Login;