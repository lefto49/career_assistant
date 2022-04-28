import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { authRoutes, profileRoutes, publicRoutes } from "../routes";

const AppRouter = (props) => {
  return (
    <Routes>
      {!props.isAuth
        ? authRoutes.map(({ path, Component }) => (
            <Route key={path} path={path} element={<Component />} />
          ))
        : profileRoutes.map(({ path, Component }) => (
            <Route key={path} path={path} element={<Component />} />
          ))}
      {publicRoutes.map(({ path, Component }) => (
        <Route key={path} path={path} element={<Component />} />
      ))}

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};

export default AppRouter;
