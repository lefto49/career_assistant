import * as axios from "axios";
import jwt_decode from "jwt-decode";

const $host = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: false
  });

  export const authApi = {
      registrationApi: {
          sendEmail: async(email)=>{
        const responce = await $host.post("get-confirmation-code/",{email});
        if (responce.status === 200){
        // localStorage.setItem("email", email);
         return "success";
        }
        return "erorr";
       }
    }
  }

