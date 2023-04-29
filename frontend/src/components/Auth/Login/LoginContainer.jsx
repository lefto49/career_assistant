import React, { useState } from "react";
import { authApi } from "../../../api/Api";
import Login from "./Login";
import { checkAuthUserData } from "../../../redux/auth-redux";
import { connect } from "react-redux";

const LoginContainer = (props) => {
  const [propperty, setPropperty] = useState({
    step: 1,
    email: "",
    password: "",
  });
  const handleFormSubmit = (e) => {
    e.preventDefault();
  };
  // const submitForm = async () => {
  //   try {
  //     let response;
  //     if (propperty.step === 1) {
  //       response = await authApi.loginApi(propperty.email, propperty.password);
  //     } else {
  //      // response = await authApi.registrationApi.sendEmail(propperty.email);
  //       response = await authApi.registrationApi.sendCode(
  //         propperty.email,
  //         propperty.code
  //       );
  //       if (response !== "erorr") {
  //         localStorage.setItem("password", propperty.password);
  //         return props.checkAuthUserData();
  //       }
  //     }
  //     if (response === "success") {
  //       setPropperty({ ...propperty, step: propperty.step + 1 });
  //     }
  //   } catch (eroor) {
  //     console.log("error!");
  //   }
  // };

  const submitForm = async () => {
    try {
      let responce;
      if (propperty.step === 1) {
        responce = await authApi.registrationApi.sendEmail(propperty.email);
        setPropperty({ ...propperty, step: propperty.step + 1 });
      } else if (propperty.step === 2) {
        responce = await authApi.registrationApi.sendCode(
          propperty.email,
          propperty.code
        );
      } else {
        responce = await authApi.loginApi(propperty.email, propperty.password);
        if (responce !== "erorr") {
          localStorage.setItem("password", propperty.password);
          return props.checkAuthUserData();
        }
      }
      if (responce === "success") {
        setPropperty({ ...propperty, step: propperty.step + 1 });
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
