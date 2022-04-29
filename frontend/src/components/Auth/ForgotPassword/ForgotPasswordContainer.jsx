import React, { useEffect, useState } from "react";
import { authApi } from "../../../api/Api";
import { connect } from "react-redux";
import ForgotPassword from "./ForgotPassword";
import { useLocation } from "react-router-dom";

const ForgotPasswordContainer = (props) => {
  let query = "";
  const [propperty, setPropperty] = useState({
    newStep: false,
    email: "",
    password: "",
    paramUid: "",
    token: "",
  });

  let { search } = useLocation();

  let id = "";
  let tokenVar = "";
  useEffect(() => {
    if (search != "" && new URLSearchParams(search)) {
      query = new URLSearchParams(search);
      if (query) {
        if (query.get("encodeUid") && query.get("token")) {
          setPropperty({ ...propperty, newStep: true });
        }
      }
    }
  }, []);

  const handleFormSubmit = (e) => {
    e.preventDefault();
  };
  const submitForm = async () => {
    try {
      let responce;
      responce = await authApi.forgotPasswordApi(propperty.email);
      if (responce === "erorr") {
        console.log("erorr from forgot password");
      } else {
        window.location.href = "/";
      }
    } catch (eroor) {
      console.log("erorr from forgot password!");
    }
  };

  const sendNewData = async () => {
    try {
      let responce;
      query = new URLSearchParams(search);
      id = query.get("encodeUid");
      tokenVar = query.get("token");
      responce = await authApi.sendNewData(id, tokenVar, propperty.password);
      if (responce === "erorr") {
        console.log("erorr from forgot password");
      } else {
        window.location.href = "/";
      }
    } catch (eroor) {
      console.log("erorr from forgot password!");
    }
  };

  return (
    <ForgotPassword
      {...props}
      propperty={propperty}
      setPropperty={setPropperty}
      handleFormSubmit={handleFormSubmit}
      submitForm={submitForm}
      sendNewData={sendNewData}
    />
  );
};

let mapStateToProps = () => {
  return {};
};

export default connect(mapStateToProps, {})(ForgotPasswordContainer);
