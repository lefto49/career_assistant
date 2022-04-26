import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import store from './redux/redux-store';
import AppContainer from './AppContainer';

const page = ReactDOM.createRoot(document.getElementById('page'));
page.render(
<Provider store={store}>
  <AppContainer/>
</Provider>
);


