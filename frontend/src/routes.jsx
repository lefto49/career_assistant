import AchievementContainer from "./components/Achievement/AchievementContainer";
import ForgotPasswordContainer from "./components/Auth/ForgotPassword/ForgotPasswordContainer";
import LoginContainer from "./components/Auth/Login/LoginContainer";
import RegistrationContainer from "./components/Auth/Registration/RegistrationContainer";
import MainPage from "./components/MainPage/MainPage";
import ProfileContainer from "./components/Profile/ProfileContainer";
import VerdictContainer from "./components/Verdict/VerdictContainer";

export const authRoutes = [
  {
    path: "/login",
    Component: LoginContainer,
  },
  {
    path: "/registration",
    Component: RegistrationContainer,
  },
  {
    path: "/forgotPassword",
    Component: ForgotPasswordContainer,
  },
];

export const profileRoutes = [
  {
    path: "/profile",
    Component: ProfileContainer,
  },
  {
    path: "/recommendations",
    Component: AchievementContainer,
  },
  {
    path: "/verdict",
    Component: VerdictContainer,
  },
];

export const publicRoutes = [
  {
    path: "/",
    Component: MainPage,
  },
];
