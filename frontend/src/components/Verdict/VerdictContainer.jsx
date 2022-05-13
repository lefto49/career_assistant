import React from "react";
import { getVerdictData } from "../../redux/verdict-redux";
import { connect } from "react-redux";
import { useEffect } from "react";
import Verdict from "./Verdict";

const VerdictContainer = (props) => {
  useEffect(() => {
    props.getVerdictData();
  }, []);
  return <Verdict {...props} />;
};

let mapStateToProps = (state) => {
  return {
    verdict: state.verdict,
  };
};
export default connect(mapStateToProps, { getVerdictData })(VerdictContainer);
