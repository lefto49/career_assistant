import { profileApi } from "../api/Api";

const SET_VERDICT_DATA = "SET-VERDICT-DATA";

let initialState = {
  verdict: null
};

const verdictReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_VERDICT_DATA: {
      return {
        ...state,
        verdict: action.data.verdict,
      };
    }
    default:
      return state;
  }
};

export const setVerdictData = ({verdict}) => ({
  type: SET_VERDICT_DATA,
  data: {
    verdict
  },
});

export const getVerdictData = () => (dispatch) => {
  return profileApi.getVerdict().then((responce) => {
    dispatch(setVerdictData(responce.data));
  });
};

export default verdictReducer;
