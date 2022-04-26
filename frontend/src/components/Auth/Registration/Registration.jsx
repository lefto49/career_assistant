import React from 'react'
import { NavLink } from 'react-router-dom';
import "./../style.css";

const Registration = (props) => {
  console.log(props);
  return (
    <form className ="form" onSubmit={(e)=>{
      props.handleFormSubmit(e);
    }}>
      <h1>Registration</h1>
      <div className ="input-form">
        <input type="text" placeholder="Email" value={props.field.email} onChange ={(e)=>{
          props.setField({...props.field,email: e.target.value});
        }}/>
      </div>
      <div className="input-form">
        <input type="submit" value="Submit" onClick={(e)=>{
          e.preventDefault(); 
          props.submitForm();
        }}/>
      </div>
      <NavLink to="">Забыли пароль?</NavLink>
      <NavLink to="">Регистрация</NavLink>
    </form>
  )
}

export default Registration;