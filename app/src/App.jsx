import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Auth from "./pages/auth/Auth"
import Homepage from "./pages/homepage/Homepage";
import Penny from "./pages/penny/Penny"

function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/homepage" element={<Homepage />} /> */}
        {/* <Route path="/login" element={<Auth />} /> */}
        {/* <Route path="/goals" element={} />*/}
        {/* <Route path="/transactions" element={} />*/}
        {/* <Route path="/budget" element={} />*/}
        {/* <Route path="/penny" element={} /> */}
        {/* <Route path="/" element={<Navigate to="/login" />} /> */}
        <Route path="/penny" element={<Penny />} />
      </Routes>
    </Router>
  );
}
export default App
