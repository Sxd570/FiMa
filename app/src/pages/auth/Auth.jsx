import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {loginService, signUpService} from '../../services/auth';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginService(email, password);
      if (data.status === "success"){
        navigate("/homepage")
      } else {
        console.error(data.status)
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleSignUpSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await signUpService(username, email, password);
      if (data.status === "success"){
        navigate("/login")
      } else {
        console.error(data.status)
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div>
      <h2>{isLogin ? 'Login' : 'Signup'}</h2>
      <form onSubmit={isLogin ? handleLoginSubmit : handleSignUpSubmit}>
        {!isLogin && (
          <div>
            <label>Name:</label>
            <input 
              type="text" 
              placeholder="Enter your name" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
            />
          </div>
        )}
        
        <div>
          <label>Email:</label>
          <input 
            type="email" 
            placeholder="Enter your email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
          />
        </div>

        <div>
          <label>Password:</label>
          <input 
            type="password" 
            placeholder="Enter your password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
          />
        </div> 
        
        <button type="submit">{isLogin ? 'Login' : 'Sign Up'}</button>
      </form>
      
      <p>
        {isLogin ? "Don't have an account? " : "Already have an account? "}
        <Link to="#" onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Sign Up' : 'Log In'}
        </Link>
      </p>
    </div>
  );
}