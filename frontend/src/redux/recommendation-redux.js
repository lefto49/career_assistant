import { profileApi } from "../api/Api";
const SET_RECOMMENDATION_DATA = "SET-RECOMMENDATION-DATA";

let initialState = {
  vacancies: null,
  cups: null,
  courses: null,
};

const recommendReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_RECOMMENDATION_DATA: {
      return {
        ...state,
        vacancies: action.data.vacancies,
        cups: action.data.cups,
        courses: action.data.courses,
      };
    }
    default:
      return state;
  }
};

export const setRecommendData = ({vacancies, cups, courses}) => ({
  type: SET_RECOMMENDATION_DATA,
  data: {
    vacancies,
    cups,
    courses,
  },
});

export const getRecommendationData = () => (dispatch) => {
  return profileApi.getRecommendations().then((responce) => {
    dispatch(setRecommendData(responce.data));
  });
};

export default recommendReducer;
