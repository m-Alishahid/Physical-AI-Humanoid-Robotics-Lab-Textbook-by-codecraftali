import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

interface AuthButtonsProps {
  onAuthChange?: (user: any) => void;
}

const AuthButtons: React.FC<AuthButtonsProps> = ({ onAuthChange }) => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<any>(null);

  // Check for existing auth token on component mount
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      // TODO: Validate token with backend and get user info
      // For now, assume token is valid and set logged in state
      setIsLoggedIn(true);
      // You might want to decode JWT or fetch user info here
    }
  }, []);

  const handleLogin = async (email: string, password: string) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('auth_token', data.access_token);
        setIsLoggedIn(true);
        setUser(data.user);
        setShowLoginModal(false);
        onAuthChange?.(data.user);
      } else {
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed. Please try again.');
    }
  };

  const handleSignup = async (formData: any) => {
    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('auth_token', data.access_token);
        setIsLoggedIn(true);
        setUser(data.user);
        setShowSignupModal(false);
        onAuthChange?.(data.user);
      } else {
        alert('Signup failed. Please try again.');
      }
    } catch (error) {
      console.error('Signup error:', error);
      alert('Signup failed. Please try again.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    setIsLoggedIn(false);
    setUser(null);
    onAuthChange?.(null);
  };

  if (isLoggedIn && user) {
    return (
      <div className={styles.authContainer}>
        <span className={styles.userInfo}>
          Welcome, {user.full_name || user.email}!
        </span>
        <button
          className={styles.logoutButton}
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>
    );
  }

  return (
    <>
      <div className={styles.authButtons}>
        <button
          className={styles.loginButton}
          onClick={() => setShowLoginModal(true)}
        >
          Login
        </button>
        <button
          className={styles.signupButton}
          onClick={() => setShowSignupModal(true)}
        >
          Sign Up
        </button>
      </div>

      {/* Login Modal */}
      {showLoginModal && (
        <LoginModal
          onClose={() => setShowLoginModal(false)}
          onLogin={handleLogin}
        />
      )}

      {/* Signup Modal */}
      {showSignupModal && (
        <SignupModal
          onClose={() => setShowSignupModal(false)}
          onSignup={handleSignup}
        />
      )}
    </>
  );
};

interface LoginModalProps {
  onClose: () => void;
  onLogin: (email: string, password: string) => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ onClose, onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onLogin(email, password);
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h3>Login</h3>
          <button className={styles.closeButton} onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit} className={styles.modalBody}>
          <div className={styles.formGroup}>
            <label htmlFor="login-email">Email</label>
            <input
              id="login-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="login-password">Password</label>
            <input
              id="login-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className={styles.primaryButton}>
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

interface SignupModalProps {
  onClose: () => void;
  onSignup: (formData: any) => void;
}

const SignupModal: React.FC<SignupModalProps> = ({ onClose, onSignup }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    python_level: 'beginner',
    robotics_experience: 'none'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSignup(formData);
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h3>Sign Up</h3>
          <button className={styles.closeButton} onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit} className={styles.modalBody}>
          <div className={styles.formGroup}>
            <label htmlFor="signup-email">Email *</label>
            <input
              id="signup-email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="signup-password">Password *</label>
            <input
              id="signup-password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="signup-name">Full Name</label>
            <input
              id="signup-name"
              name="full_name"
              type="text"
              value={formData.full_name}
              onChange={handleChange}
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="python-level">Python Level *</label>
            <select
              id="python-level"
              name="python_level"
              value={formData.python_level}
              onChange={handleChange}
              required
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
              <option value="expert">Expert</option>
            </select>
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="robotics-exp">Robotics Experience *</label>
            <select
              id="robotics-exp"
              name="robotics_experience"
              value={formData.robotics_experience}
              onChange={handleChange}
              required
            >
              <option value="none">None</option>
              <option value="basic">Basic</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
              <option value="expert">Expert</option>
            </select>
          </div>
          <button type="submit" className={styles.primaryButton}>
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
};

export default AuthButtons;
