import * as React from "react";
import "./styles.css";
import logo from "./logo.png";

export default function App({ onChange }) {
  return (
    <div className="MicroApp">
      <div>
        <img src={logo} alt={"logo"} className="center-img" />
      </div>
    </div>
  );
}
