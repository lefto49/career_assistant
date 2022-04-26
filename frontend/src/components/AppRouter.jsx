import React from 'react'
import { Route, Routes } from 'react-router-dom';
import { authRoutes, publicRoutes } from '../routes';

const AppRouter = () => {
  return (
     <Routes>
       {
           authRoutes.map(({path,Component})=>(
             <Route key = {path} path = {path} element = {<Component/>}/>
           ))
       },
       {
          publicRoutes.map(({path,Component})=>(
            <Route key = {path} path = {path} element = {<Component/>}/>
          ))
       }
     </Routes>
  )
}

export default AppRouter;