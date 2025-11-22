import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import styles from "./Sidebar.module.css";

import {
  LayoutDashboard,
  Receipt,
  Target,
  BarChart2,
  Calendar,
  Bot,
  ChevronLeft,
  ChevronRight
} from "lucide-react";

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  const navItems = [
    { label: "Home", to: "/home", icon: <LayoutDashboard size={20} /> },
    { label: "Transactions", to: "/transactions", icon: <Receipt size={20} /> },
    { label: "Goals", to: "/goals", icon: <Target size={20} /> },
    { label: "Reports", to: "/reports", icon: <BarChart2 size={20} /> },
    { label: "Budgets", to: "/budget", icon: <Calendar size={20} /> },
    { label: "PennyAI", to: "/penny", icon: <Bot size={20} /> },
  ];

  return (
    <aside className={`${styles.sidebar} ${collapsed ? styles.collapsed : ""}`}>
      
      <button
        className={styles.toggle}
        onClick={() => setCollapsed((prev) => !prev)}
      >
        {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      <nav className={styles.nav}>
        <ul className={styles.menu}>
          {navItems.map((item, index) => (
            <React.Fragment key={item.label}>
              <li>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    isActive ? `${styles.link} ${styles.active}` : styles.link
                  }
                >
                  <span className={styles.icon}>{item.icon}</span>
                  {!collapsed && item.label}
                </NavLink>
              </li>

              {/* Add separator after PennyAI (index 0) */}
              {index === 4 && <hr className={styles.separator} />}
            </React.Fragment>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
