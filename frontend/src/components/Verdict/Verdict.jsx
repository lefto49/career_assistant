import React from "react";

const Verdict = (props) => {
  let PrintVerdict = () => {
    if (props.verdict.verdict) {
      return (
        <div
          style={{
            backgroundColor: "#006400",
            marginBottom: "20px",
            border: "1px solid white",
            padding: "10px",
          }}
        >
          <h1>{props.verdict.verdict}</h1>
        </div>
      );
    }
  };

  return (
    <>
      <h1
        style={{
          fontSize: "30px",
          textAlign: "center",
          marginBottom: "40px",
          marginTop: "40px",
        }}
      >
        Verdict
      </h1>
      {PrintVerdict()}
    </>
  );
};

export default Verdict;
