import { applyMiddleware, combineReducers, createStore } from "redux";
import thunkMiddleware from "redux-thunk";
import authReducer from "./auth-redux";
import profileReducer from "./profile-redux";


let reducers = combineReducers({
    auth: authReducer,
    profile: profileReducer
});

let store = createStore(reducers, applyMiddleware(thunkMiddleware));

window.store = store;
export default store;