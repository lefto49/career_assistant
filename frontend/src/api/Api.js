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
      registrationApi: async(email)=>{
       const {data} = await $host.post("get-confirmation-code/",{email});
       return data;
      }
  }