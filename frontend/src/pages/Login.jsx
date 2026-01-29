import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Login endpoint expects form data (OAuth2PasswordRequestForm)
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const response = await api.post('/auth/token', formData);
            login(response.data.access_token);
            navigate('/');
        } catch (err) {
            console.error("Login Error:", err);
            const errorMessage = err.response?.data?.detail || 'Invalid email or password';
            setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
        }
    };

    return (
        <div className="flex-center" style={{ minHeight: '100vh', backgroundColor: 'var(--bg-main)' }}>
            <div className="card" style={{ width: '100%', maxWidth: '400px' }}>
                <h2 style={{ textAlign: 'center', color: 'var(--text-primary)', marginBottom: '1.5rem' }}>NutriTrack Login</h2>
                {error && <p style={{ color: 'var(--accent)', textAlign: 'center', marginBottom: '1rem' }}>{error}</p>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Email Address</label>
                        <input
                            type="email"
                            className="input-field"
                            placeholder="you@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            className="input-field"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
                        Sign In
                    </button>
                    <p style={{ textAlign: 'center', marginTop: '1rem', fontSize: '0.9rem' }}>
                        Don't have an account? <Link to="/register" style={{ color: 'var(--secondary)', textDecoration: 'none' }}>Register</Link>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default Login;
