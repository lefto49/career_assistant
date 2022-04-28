import React from "react";
import { NavLink } from "react-router-dom";

const Profile = (props) => {
  return (
    <>
      <form
        className="form"
        onSubmit={(e) => {
          props.handleFormSubmit(e);
        }}
      >
        <h1>Profile</h1>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="Email"
            name="email"
            value={props.profile.email}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="Last_name"
            name="last_name"
            value={props.profile.last_name}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="First_name"
            name="first_name"
            value={props.profile.first_name}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="Birth_year"
            name="birth_year"
            value={props.profile.birth_year}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="city"
            name="city"
            value={props.profile.city}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="university"
            name="university"
            value={props.profile.university}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="vacancy"
            name="vacancy"
            value={props.profile.vacancy}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          <input
            disabled={!props.activeChange}
            type="text"
            placeholder="experience"
            name="experience"
            value={props.profile.experience}
            onChange={(e) => {
              props.setProfileUserData({
                ...props.profile,
                [e.target.getAttribute("name")]: e.target.value,
              });
            }}
          />
        </div>
        <div className="input-form">
          {!props.activeChange && (
            <input
              type="button"
              value="Change your data"
              onClick={() => {
                props.setActiveChange(true);
              }}
            />
          )}
        </div>
        <div className="input-form">
          {props.activeChange && (
            <input
              type="submit"
              value="Save"
              onClick={(e) => {
                e.preventDefault();
                props.setActiveChange(false);
                props.submitForm();
              }}
            />
          )}
        </div>
      </form>
    </>
  );
};

export default Profile;
