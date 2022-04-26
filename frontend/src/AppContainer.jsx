import React from 'react'
import App from './App'
import { checkAuthUserData } from './redux/auth-redux'

const AppContainer = () => {
  return (
     <App/>
  )
}

let mapStateToProps = (state) => {
    return {
    //  isAuth: state.auth.isAuth,
    };
  };


export default AppContainer;