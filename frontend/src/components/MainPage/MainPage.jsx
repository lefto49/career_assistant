import logo from "./logo.png";
import React, { lazy, Suspense } from "react";

const MainPage = () => {
  // const Main = lazy(() => import("FIRST_APP/app"));
  return (
    <div>
      {/* <Main /> */}
      <img src={logo} alt={"logo"} className="center-img" />
    </div>
  );
};

export default MainPage;
