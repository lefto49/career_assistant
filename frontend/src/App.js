import React from 'react';
import './App.scss';
import Header from './components/Header/Header';
import { BrowserRouter } from "react-router-dom";
import AppRouter from './components/AppRouter';

const App=(props) => {
  return (
    <BrowserRouter>
     <Header/>
     <AppRouter/>
    </BrowserRouter>
  );
} 

export default App;
