import React from 'react';
import { Link } from 'react-router-dom';

export default function Sidebar() {
  return (
    <div>
      <h3>Navigation</h3>
      <nav>
        <ul>
          <li><Link to="/home">Home</Link></li>
          <li><Link to="/budget">Budget</Link></li>
          <li><Link to="/transactions">Transactions</Link></li>
          <li><Link to="/goals">Goals</Link></li>
          <li><Link to="/penny">Penny</Link></li>
          <li><Link to="/settings">Settings</Link></li>
        </ul>
      </nav>
    </div>
  );
}
