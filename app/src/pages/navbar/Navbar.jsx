import React, { useState, useRef, useEffect } from "react";
import styles from "./Navbar.module.css";
import { Settings, LogOut, User } from "lucide-react";

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <header className={styles.navbar}>
      <div className={styles.title}>Penny</div>

      <div className={styles.actions} ref={dropdownRef}>
        
        <button
          className={styles.iconButton}
          onClick={() => setOpen((prev) => !prev)}
        >
          <User size={20} />
        </button>

        {open && (
          <div className={styles.dropdown}>
            <button className={styles.dropdownItem}>
              <User size={16} /> My Profile
            </button>
            <button className={styles.dropdownItem}>
              <Settings size={16} /> Settings
            </button>
            <button className={styles.dropdownItem}>
              <LogOut size={16} /> Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
