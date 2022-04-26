import Login from "./components/Auth/Login/Login";
import RegistrationContainer from "./components/Auth/Registration/RegistrationContainer";
import MainPage from "./components/MainPage/MainPage";

export const authRoutes = [
    {
        path: "/login",
        Component: Login
    },
    {
        path: "/registration",
        Component: RegistrationContainer
    }
]

export const publicRoutes = [
    {
        path: "/",
        Component: MainPage
    }
]