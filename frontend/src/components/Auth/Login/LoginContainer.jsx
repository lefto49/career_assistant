import React, { useState } from "react";
import { authApi } from "../../../api/Api";
import Login from "./Login";
import { checkAuthUserData } from "../../../redux/auth-redux";
import { connect } from "react-redux";

const LoginContainer = (props) => {
  const [propperty, setPropperty] = useState({
    email: "",
    password: "",
  });
  const handleFormSubmit = (e) => {
    e.preventDefault();
  };
  const submitForm = async () => {
    try {
      let responce;
      responce = await authApi.loginApi(propperty.email, propperty.password);
      if (responce !== "erorr") {
        localStorage.setItem("password", propperty.password);
        return props.checkAuthUserData();
      }
    } catch (eroor) {
      console.log("error!");
    }
  };
  return (
    <Login
      {...props}
      propperty={propperty}
      setPropperty={setPropperty}
      handleFormSubmit={handleFormSubmit}
      submitForm={submitForm}
    />
  );
};

let mapStateToProps = () => {
  return {};
};

export default connect(mapStateToProps, { checkAuthUserData })(LoginContainer);
