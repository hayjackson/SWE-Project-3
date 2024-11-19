import React from "react";

const Home = () => {
  return (
    <div
      style={{
        textAlign: "center",
        margin: "40px auto",
        maxWidth: "600px",
        padding: "20px",
        backgroundColor: "#f9f9f9",
        borderRadius: "8px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
      }}
    >
      <h1
        style={{
          fontSize: "2.5rem",
          color: "#333",
          marginBottom: "10px",
        }}
      >
        Welcome to ReviewMaster
      </h1>
      <p
        style={{
          fontSize: "1.1rem",
          color: "#666",
          marginBottom: "20px",
        }}
      >
        Your trusted platform to rate, review, and discover the best books,
        movies, and TV shows.
      </p>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          marginTop: "30px",
        }}
      >
        <div style={{ textAlign: "left" }}>
          <h3 style={{ color: "#555" }}>Why Use ReviewMaster?</h3>
          <ul
            style={{
              listStyleType: "circle",
              paddingLeft: "20px",
              color: "#666",
            }}
          >
            <li>Share your honest reviews with others.</li>
            <li>Discover top-rated content recommended by users.</li>
            <li>Track your favorite books, movies, and shows.</li>
          </ul>
        </div>
      </div>
      <button
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "#007BFF",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          fontSize: "1rem",
          cursor: "pointer",
        }}
        onClick={() => alert("Feature coming soon!")}
      >
        Explore Now
      </button>
    </div>
  );
};

export default Home;
