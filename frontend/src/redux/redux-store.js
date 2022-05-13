import { applyMiddleware, combineReducers, createStore } from "redux";
import thunkMiddleware from "redux-thunk";
import authReducer from "./auth-redux";
import profileReducer from "./profile-redux";
import recommendReducer from "./recommendation-redux";
import verdictReducer from "./verdict-redux";

let reducers = combineReducers({
  auth: authReducer,
  profile: profileReducer,
  recommendation: recommendReducer,
  verdict: verdictReducer,
});

let store = createStore(reducers, applyMiddleware(thunkMiddleware));

window.store = store;
export default store;
