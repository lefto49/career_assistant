import React from "react";
import { NavLink } from "react-router-dom";
import "./../style.css";

const Registration = (props) => {
  //  console.log(props);
  let renderSwitch = (props) => {
    // console.log(props);
    switch (props.propperty.step) {
      case 1: {
        return <SendEmail {...props} />;
      }
      case 2: {
        return <ConfirmEmail {...props} />;
      }
      case 3: {
        return <SetAllData {...props} />;
      }
      default:
        return <SendEmail {...props} />;
    }
  };
  return renderSwitch(props);
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
      <h1>Registration</h1>
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

const SetAllData = (props) => {
  return (
    <form
      className="form"
      onSubmit={(e) => {
        props.handleFormSubmit(e);
      }}
    >
      <h1>Write your another information</h1>
      <div className="input-form">
        <input
          type="text"
          placeholder="Lastname"
          value={props.propperty.last_name}
          onChange={(e) => {
            props.setPropperty({
              ...props.propperty,
              last_name: e.target.value,
            });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="text"
          placeholder="Firstname"
          value={props.propperty.first_name}
          onChange={(e) => {
            props.setPropperty({
              ...props.propperty,
              first_name: e.target.value,
            });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="number"
          placeholder="Birth year"
          value={props.propperty.birth_year}
          onChange={(e) => {
            props.setPropperty({
              ...props.propperty,
              birth_year: e.target.value,
            });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="text"
          placeholder="City"
          value={props.propperty.city}
          onChange={(e) => {
            props.setPropperty({ ...props.propperty, city: e.target.value });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="text"
          placeholder="University"
          value={props.propperty.university}
          onChange={(e) => {
            props.setPropperty({
              ...props.propperty,
              university: e.target.value,
            });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="text"
          placeholder="Vacancy"
          value={props.propperty.vacancy}
          onChange={(e) => {
            props.setPropperty({ ...props.propperty, vacancy: e.target.value });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="text"
          placeholder="Experience"
          value={props.propperty.experience}
          onChange={(e) => {
            props.setPropperty({
              ...props.propperty,
              experience: e.target.value,
            });
          }}
        />
      </div>
      <div className="input-form">
        <input
          type="password"
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

export default Registration;
