import React from "react";
import { getRecommendationData } from "../../redux/recommendation-redux";
import Achievement from "./Achievement";
import { connect } from "react-redux";
import { useEffect } from "react";

const AchievementContainer = (props) => {
  useEffect(() => {
    props.getRecommendationData();
  }, []);
  console.log(props);
  return <Achievement {...props} />;
};

let mapStateToProps = (state) => {
  return {
    recommendation: state.recommendation,
  };
};
export default connect(mapStateToProps, { getRecommendationData })(
  AchievementContainer
);
