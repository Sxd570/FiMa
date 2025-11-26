import React, { useState } from "react";
import { useLocation, Navigate } from "react-router-dom";
import styles from "./Dashboard.module.css";

import Sidebar from "../sidebar/Sidebar";
import Navbar from "../navbar/Navbar";
import Homepage from "../homepage/Homepage";
import Penny from "../penny/Penny";
import Transaction from "../transaction/Transaction";
import Budget from "../budget/Budget";
import Goal from "../goal/Goal";
import Report from "../report/Report";

export default function Dashboard() {
  const location = useLocation();

  const renderContent = () => {
    switch (location.pathname) {
      case "/home":
        return <Homepage />;
      case "/transactions":
        return <Transaction />;
      case "/goals":
        return <Goal />;
      case "/reports":
        return <Report />;
      case "/budget":
        return <Budget />;
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
