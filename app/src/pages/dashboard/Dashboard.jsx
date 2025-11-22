import React, { useState } from "react";
import styles from "./Dashboard.module.css";

import Sidebar from "../sidebar/Sidebar";
import Navbar from "../navbar/Navbar";
import Homepage from "../homepage/Homepage";
import Penny from "../penny/Penny";

export default function Dashboard() {

  return (
    <div className={styles.dashboard}>
      <Navbar />
      <Sidebar />
      <main
        className={styles.mainContent}
      >
        <h1>Dashboard</h1>
      </main>
    </div>
  );
}
