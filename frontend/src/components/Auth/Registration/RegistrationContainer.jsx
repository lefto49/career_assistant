import React, { useState } from 'react'
import { authApi } from '../../../api/Api';
import Registration from './Registration';

const RegistrationContainer = (props) => {
    const [field, setField] = useState({
        email: "",
          });
    const handleFormSubmit = (e) => {
    e.preventDefault();
  };
  const submitForm = async() => {
      try{
        let data = await authApi.registrationApi(field.email);
      }
      catch(eroor){
         console.log("error!")
      }
  }
  return (
    <Registration {...props} field = {field} setField = {setField} handleFormSubmit = {handleFormSubmit} submitForm = {submitForm} />
  )
}

let mapStateToProps = () => {
    return {
    
    };
  };


export default RegistrationContainer;