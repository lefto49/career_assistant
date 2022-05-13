import React from "react";
import {
  getProfileUserData,
  setProfileUserData,
} from "../../redux/profile-redux";
import Profile from "./Profile";
import { connect } from "react-redux";
import { useEffect, useState } from "react";
import { profileApi } from "../../api/Api";

const ProfileContainer = (props) => {
  const [activeChange, setActiveChange] = useState(false);
  useEffect(() => {
    props.getProfileUserData();
  }, []);

  const handleFormSubmit = (e) => {
    e.preventDefault();
  };

  const submitForm = async () => {
    try {
      let responce;
      responce = await profileApi.putNewUserUpdate(props.profile);
      if (responce !== "erorr") {
        return props.setProfileUserData(responce.data);
      }
    } catch (eroor) {
      console.log("error!");
    }
  };

  return (
    <Profile
      {...props}
      activeChange={activeChange}
      setActiveChange={setActiveChange}
      handleFormSubmit={handleFormSubmit}
      submitForm={submitForm}
    />
  );
};

let mapStateToProps = (state) => {
  return {
    profile: state.profile,
  };
};

export default connect(mapStateToProps, {
  getProfileUserData,
  setProfileUserData,
})(ProfileContainer);
