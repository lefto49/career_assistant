import * as axios from "axios";
import jwt_decode from "jwt-decode";

const $host = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false,
});

const $authHost = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

const authInterceptor = (config) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem("access")}`;
  return config;
};

$authHost.interceptors.request.use(authInterceptor);

export const profileApi = {
  getUserDataApi: async () => {
    const responce = await $authHost.get("profile/");
    if (responce.status === 200) {
      return responce;
    }
    return null;
  },

  putNewUserUpdate: async (data) => {
    const password = localStorage.getItem("password");
    data.password = password;
    const responce = await $authHost.put("profile/", data);
    if (responce.status === 200) {
      return responce;
    }
    return null;
  },
}

export const authApi = {
  loginApi: async (email, password) => {
    const responce = await $host.post("login/", { email, password });
    if (responce.status >= 200 && responce.status < 300) {
      localStorage.setItem("access", responce.data.access);
      localStorage.setItem("refresh", responce.data.refresh);
      return responce.data.user;
    }
    return "erorr";
  },
  checkApi: async () => {
    const responce = await $authHost.get("profile/");
    if (responce.status === 200) {
      return "success";
    }
    return "erorr";
  },

  registrationApi: {
    sendEmail: async (email) => {
      const responce = await $host.post("get-confirmation-code/", { email });
      if (responce.status === 200) {
        // localStorage.setItem("email", email);
        return "success";
      }
      return "erorr";
    },
    sendCode: async (email, code) => {
      const responce = await $host.post("confirm-email/", { email, code });
      if (responce.status === 200) {
        return "success";
      }
      return "erorr";
    },
    sendUserData: async (
      last_name,
      first_name,
      birth_year,
      city,
      university,
      vacancy,
      experience,
      email,
      password
    ) => {
      const responce = await $host.post("signup/", {
        last_name,
        first_name,
        birth_year,
        city,
        university,
        vacancy,
        experience,
        email,
        password,
      });

      if (responce.status >= 200 && responce.status < 300) {
        localStorage.setItem("access", responce.data.access);
        localStorage.setItem("refresh", responce.data.refresh);
        return responce.data.user;
      }
      return "erorr";
    },
  },
};
