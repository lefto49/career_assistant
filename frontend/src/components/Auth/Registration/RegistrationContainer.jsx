import React, { useState } from "react";
import { authApi } from "../../../api/Api";
import Registration from "./Registration";
import { checkAuthUserData } from "../../../redux/auth-redux";
import { connect } from "react-redux";

const RegistrationContainer = (props) => {
  const [propperty, setPropperty] = useState({
    step: 1,
    email: "",
    code: "",
    last_name: "",
    first_name: "",
    birth_year: "",
    city: "",
    university: "",
    vacancy: "",
    experience: "",
    password: "",
  });
  const handleFormSubmit = (e) => {
    e.preventDefault();
  };
  const submitForm = async () => {
    try {
      let responce;
      if (propperty.step === 1) {
        responce = await authApi.registrationApi.sendEmail(propperty.email);
      } else if (propperty.step === 2) {
        responce = await authApi.registrationApi.sendCode(
          propperty.email,
          propperty.code
        );
      } else {
        responce = await authApi.registrationApi.sendUserData(
          propperty.last_name,
          propperty.first_name,
          propperty.birth_year,
          propperty.city,
          propperty.university,
          propperty.vacancy,
          propperty.experience,
          propperty.email,
          propperty.password
        );
        if (responce !== "erorr") {
          localStorage.setItem("password", propperty.password);
          console.log(responce);
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
    <Registration
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

export default connect(mapStateToProps, { checkAuthUserData })(
  RegistrationContainer
);
