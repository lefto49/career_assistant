
const SET_AUTH_USER_DATA = "SET-AUTH-USER-DATA";

let initialState = {
    isAuth: false,
};

  const authReducer = (state = initialState, action) => {
    switch (action.type) {
      case SET_AUTH_USER_DATA: {
        return {
          ...state,
          isAuth: action.data.isAuth,
        };
      }
      default:
        return state;
    }
  };

export const setAuthUserData=(isAuth)=>({
    type: SET_AUTH_USER_DATA,
    data: {
        isAuth
    }
})

export const checkAuthUserData=()=>(dispatch)=>{
   return setAuthUserData(true);
}

export default authReducer;