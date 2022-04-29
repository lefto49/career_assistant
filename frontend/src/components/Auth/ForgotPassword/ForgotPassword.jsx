import React from "react";
import "./../style.css";

const ForgotPassword = (props) => {
  return (
    <>
      {!props.propperty.newStep ? (
        <form className="form">
          <h1>Forgot password</h1>
          <div className="input-form">
            <input
              type="text"
              placeholder="Email"
              value={props.propperty.email}
              onChange={(e) => {
                props.setPropperty({
                  ...props.propperty,
                  email: e.target.value,
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
        </form>
      ) : (
        <form className="form">
          <h1>Enter new password</h1>
          <div className="input-form">
            <input
              type="text"
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
                props.sendNewData();
              }}
            />
          </div>
        </form>
      )}
    </>
  );
};

export default ForgotPassword;
