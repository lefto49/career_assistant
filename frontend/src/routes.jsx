import ForgotPassword from "./components/Auth/ForgotPassword/ForgotPassword";
import ForgotPasswordContainer from "./components/Auth/ForgotPassword/ForgotPasswordContainer";
import Login from "./components/Auth/Login/Login";
import LoginContainer from "./components/Auth/Login/LoginContainer";
import RegistrationContainer from "./components/Auth/Registration/RegistrationContainer";
import MainPage from "./components/MainPage/MainPage";
import ProfileContainer from "./components/Profile/ProfileContainer";

export const authRoutes = [
    {
        path: "/login",
        Component: LoginContainer
    },
    {
        path: "/registration",
        Component: RegistrationContainer
    },
    {
        path: "/forgotPassword",
        Component: ForgotPasswordContainer
    }
]

export const profileRoutes = [
    {
        path: "/profile",
        Component: ProfileContainer
    }
]

export const publicRoutes = [
    {
        path: "/",
        Component: MainPage
    }
]