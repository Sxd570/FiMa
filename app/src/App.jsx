import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import styles from './App.module.css';

import Auth from "./pages/auth/Auth"
import Dashboard from "./pages/dashboard/Dashboard";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/*" element={<Dashboard />} />
        {/* <Route path="/login" element={<Auth />} /> */}
      </Routes>
    </Router>
  );
}
export default App
