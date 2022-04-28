import { profileApi } from "../api/Api";

const GET_PROFILE_USER_DATA = "GET-PROFILE-USER-DATA";

let initialState = {
  id: "",
  email: "",
  last_name: "",
  first_name: "",
  birth_year: "",
  city: "",
  university: "",
  vacancy: "",
  experience: "",
  password: "",
};

const profileReducer = (state = initialState, action) => {
  switch (action.type) {
    case GET_PROFILE_USER_DATA: {
      return {
        ...state,
        ...action.data,
      };
    }
    default:
      return state;
  }
};

export const setProfileUserData = ({
  id,
  email,
  last_name,
  first_name,
  birth_year,
  city,
  university,
  vacancy,
  experience,
  password,
}) => ({
  type: GET_PROFILE_USER_DATA,
  data: {
    id,
    email,
    last_name,
    first_name,
    birth_year,
    city,
    university,
    vacancy,
    experience,
    password,
  },
});

export const getProfileUserData = () => (dispatch) => {
  return profileApi.getUserDataApi().then((responce) => {
    console.log(responce);
    console.log(responce.data);
    if (responce !== null) {
      dispatch(setProfileUserData(responce.data));
    }
  });
};

export default profileReducer;
