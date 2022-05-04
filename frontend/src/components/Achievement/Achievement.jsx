import React from "react";
import { Link } from "react-router-dom";

const Achievement = (props) => {
  let PrintCourses = () => {
    if (props.recommendation.courses) {
      return props.recommendation.courses.map((course, index) => {
        return (
          <div
            key={index}
            style={{
              backgroundColor: "#006400",
              marginBottom: "20px",
              border: "1px solid white",
              padding: "10px",
            }}
          >
            <h1>{course.title}</h1>
            <br/>
            <p>{course.description}</p>
            <br/>
            <a href={course.link}>{course.link}</a>
          </div>
        );
      });
    }
  };

  let PrintCups = () => {
    if (props.recommendation.cups) {
      return props.recommendation.cups.map((cup, index) => {
        return (
          <div
            key={index}
            style={{
              backgroundColor: "#006400",
              marginBottom: "20px",
              border: "1px solid white",
              padding: "10px",
            }}
          >
            <h1>{cup.title}</h1>
            <br/>
            <p>{cup.description}</p>
            <br/>
            <a href={cup.link}>{cup.link}</a>
          </div>
        );
      });
    }
  };

  let PrintVacancies = () => {
    if (props.recommendation.vacancies) {
      return props.recommendation.vacancies.map((vacancie, index) => {
        return (
          <div
            key={index}
            style={{
              backgroundColor: "#006400",
              marginBottom: "20px",
              border: "1px solid white",
              padding: "10px",
            }}
          >
            <h1>{vacancie.title}</h1>
            <br/>
            <p>{vacancie.description}</p>
          </div>
        );
      });
    }
  };
  
  return (
    <>
      <h1  style={{
              fontSize: "30px", textAlign: "center",
              marginBottom: "40px", marginTop: "40px",
            }}>Courses</h1>
      {PrintCourses()}

      <h1  style={{
              fontSize: "30px", textAlign: "center",
              marginBottom: "40px", marginTop: "40px",
            }}>Cups</h1>
      {PrintCups()}

      <h1  style={{
              fontSize: "30px", textAlign: "center",
              marginBottom: "40px", marginTop: "40px",
            }}>Vacancies</h1>
      {PrintVacancies()}
    </>
  );
};

export default Achievement;
