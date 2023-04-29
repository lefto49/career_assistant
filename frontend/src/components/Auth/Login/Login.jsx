import React from "react";
import { NavLink } from "react-router-dom";
import "./../style.css";

const Login = (props) => {
  let renderSwitch = (props) => {
    console.log("122", props);
    switch (props.propperty.step) {
      case 1: {
        return <SendEmail {...props} />;
      }
      case 2: {
        return <ConfirmEmail {...props} />;
      }
      case 3: {
        return <LoginCheck {...props} />;
      }
      default:
        return <SendEmail {...props} />;
    }
  };
  return renderSwitch(props);
};

const LoginCheck = (props) => {
  return (
    <form
      className="form"
      action="#"
      onSubmit={(e) => {
        props.handleFormSubmit(e);
      }}
    >
      {/* <h1>Login</h1>
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
      </div> */}
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


const SendEmail = (props) => {
  // console.log(props);
  return (
    <form
      className="form"
      onSubmit={(e) => {
        props.handleFormSubmit(e);
      }}
    >
      <h1>Введите логин</h1>
      <div className="input-form">
        <input
          type="text"
          placeholder="Email"
          value={props.propperty.email}
          onChange={(e) => {
            props.setPropperty({ ...props.propperty, email: e.target.value });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="submit"
          value="Submit"
          onClick={(e) => {
            e.preventDefault();
            props.submitForm();
          }}
        />
      </div>
    </form>
  );
};

const ConfirmEmail = (props) => {
  return (
    <form
      className="form"
      onSubmit={(e) => {
        props.handleFormSubmit(e);
      }}
    >
      <h1>Code</h1>
      <div className="input-form">
        <input
          type="text"
          placeholder="Code"
          value={props.propperty.code}
          onChange={(e) => {
            props.setPropperty({ ...props.propperty, code: e.target.value });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="submit"
          value="Submit"
          onClick={(e) => {
            e.preventDefault();
            props.submitForm();
          }}
        />
      </div>
    </form>
  );
};

export default Login;
