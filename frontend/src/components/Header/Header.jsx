import React from 'react'
import { NavLink } from 'react-router-dom';
import "./Header.scss"

const Header = (props) => {
    return (
    <header className="header">
      <div className="header__body catalog-header">
        <div className="catalog-header__container">
          <div className="catalog-header__menu menu">
            <nav className="menu__body">
              <ul className="menu__list">
                <li className="menu__item">
                  <NavLink to="/" className="menu__link">
                    Home
                  </NavLink>
                </li>
                <li className="menu__item">
                  <NavLink to="/login" className="menu__link">
                    Sign in
                  </NavLink>
                </li>
                <li className="menu__item">
                  <NavLink to="/registration" className="menu__link">
                    Registration
                  </NavLink>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </header>
      );
}

export default Header;