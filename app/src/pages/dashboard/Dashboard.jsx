import React, { useState } from "react";
import { useLocation, Navigate } from "react-router-dom";
import styles from "./Dashboard.module.css";

import Sidebar from "../sidebar/Sidebar";
import Navbar from "../navbar/Navbar";
import Homepage from "../homepage/Homepage";
import Penny from "../penny/Penny";

export default function Dashboard() {
  const location = useLocation();

  const renderContent = () => {
    switch (location.pathname) {
      case "/home":
        return <Homepage />;
      case "/transactions":
        return <div>Transactions Page</div>;
      case "/goals":
        return <div>Goals Page</div>;
      case "/reports":
        return <div>Reports Page</div>;
      case "/budget":
        return <div>Budget Page</div>;
      case "/penny":
        return <Penny />;
      case "/":
        return <Navigate to="/home" replace />;
      default:
        return <Homepage />;
    }
  };

  return (
    <div className={styles.dashboard}>
      <Navbar />
      <Sidebar />
      <main className={styles.mainContent}>
        {renderContent()}
      </main>
    </div>
  );
}
