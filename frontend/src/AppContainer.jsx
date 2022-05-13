import React from "react";
import App from "./App";
import { checkAuthUserData } from "./redux/auth-redux";
import { connect } from "react-redux";
import { useEffect } from "react";

const AppContainer = (props) => {
  useEffect(() => {
    props.checkAuthUserData();
  }, []);
  return <App {...props} />;
};

let mapStateToProps = (state) => {
  return {
    isAuth: state.auth.isAuth,
  };
};

export default connect(mapStateToProps, {
  checkAuthUserData,
})(AppContainer);
