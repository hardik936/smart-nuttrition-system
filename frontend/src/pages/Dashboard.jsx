import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import MealForm from '../components/MealForm';
import MealList from '../components/MealList';
import Gamification from '../components/Gamification';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, Legend, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';

const Dashboard = () => {
    const { user, logout } = useAuth();
    const { theme, toggleTheme } = useTheme();
    const [logs, setLogs] = useState([]);
    const [userData, setUserData] = useState(null);
    const [weeklyStats, setWeeklyStats] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [totals, setTotals] = useState({ calories: 0, protein: 0, carbs: 0, fat: 0 });
    const [isListening, setIsListening] = useState(false);
    const [voiceResults, setVoiceResults] = useState(null); // Array of foods to confirm

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const [logsRes, userRes, statsRes] = await Promise.all([
                api.get('/api/v1/logs/'),
                api.get('/auth/me'),
                api.get('/api/v1/logs/stats/weekly')
            ]);
            setLogs(logsRes.data);
            setUserData(userRes.data);
            setWeeklyStats(statsRes.data);
            calculateTotals(logsRes.data);
            setLoading(false);
        } catch (err) {
            console.error(err);
            setError('Failed to fetch data.');
            setLoading(false);
        }
    };

    const handleVoiceLog = () => {
        if (isListening) return;

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Your browser doesn't support voice recognition.");
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.start();
        setIsListening(true);

        recognition.onresult = async (event) => {
            const text = event.results[0][0].transcript;
            setIsListening(false);

            try {
                const res = await api.post('/api/v1/logs/voice', { text });
                setVoiceResults(res.data);
            } catch (err) {
                console.error(err);
                alert("Failed to process voice command.");
            }
        };

        recognition.onend = () => setIsListening(false);
        recognition.onerror = (event) => {
            console.error(event.error);
            setIsListening(false);
        }
    };

    const confirmVoiceLog = async (foodItem) => {
        try {
            // Check if we need to create the food first (if match_found is false)
            let foodId = foodItem.id;

            if (!foodItem.match_found) {
                const createRes = await api.post('/api/v1/foods/', {
                    name: foodItem.name,
                    calories: foodItem.calories,
                    protein: foodItem.protein,
                    carbs: foodItem.carbs,
                    fat: foodItem.fat
                });
                foodId = createRes.data.id;
            }

            await api.post('/api/v1/logs/', {
                food_id: foodId,
                quantity: foodItem.quantity || 100
            });

            // Remove from results list
            setVoiceResults(prev => prev.filter(f => f !== foodItem));

            // Refresh logs
            fetchLogs();

        } catch (err) {
            console.error(err);
            alert("Failed to log item.");
        }
    };

    useEffect(() => {
        fetchLogs();
    }, []);

    if (loading) return <div className="container">Loading...</div>;

    const targetCalories = userData?.target_calories || 2000;
    const caloriesProgress = Math.min((totals.calories / targetCalories) * 100, 100);

    // Chart Data
    const macroData = [
        { name: 'Protein', value: parseFloat(totals.protein.toFixed(1)), color: '#0088FE' },
        { name: 'Carbs', value: parseFloat(totals.carbs.toFixed(1)), color: '#00C49F' },
        { name: 'Fat', value: parseFloat(totals.fat.toFixed(1)), color: '#FFBB28' },
    ];

    // Filter out zero values for cleaner chart
    const activeMacroData = macroData.filter(d => d.value > 0);

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ margin: 0 }}>NutriTrack Dashboard</h1>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <button
                        onClick={toggleTheme}
                        style={{
                            background: 'none',
                            border: 'none',
                            fontSize: '1.5rem',
                            cursor: 'pointer',
                            padding: '0.5rem',
                            borderRadius: '50%',
                            backgroundColor: 'var(--bg-hover)'
                        }}
                        title="Toggle Dark Mode"
                    >
                        {theme === 'light' ? '🌙' : '☀️'}
                    </button>
                    <span style={{ color: 'var(--text-secondary)' }}>{user?.email}</span>
                    <Link to="/profile" className="btn btn-secondary" style={{ textDecoration: 'none' }}>Profile</Link>
                    <button onClick={logout} className="btn btn-secondary">Logout</button>
                </div>
            </div>

            {/* Gamification Banner */}
            <div style={{ marginBottom: '2rem' }}>
                <Gamification
                    streak={userData?.streak_count || 0}
                    logs={logs}
                    targetCalories={targetCalories}
                    totalCalories={totals.calories}
                />
            </div>

            {/* Feature Navigation Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
                <Link to="/scan" style={{ textDecoration: 'none' }}>
                    <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s', border: '2px solid var(--primary)' }}
                        onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-4px)'}
                        onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
                        <div style={{ fontSize: '2.5rem', textAlign: 'center', marginBottom: '0.5rem' }}>📸</div>
                        <h3 style={{ margin: '0 0 0.5rem 0', color: 'var(--primary)', textAlign: 'center' }}>Scan Label</h3>
                        <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.9rem', textAlign: 'center' }}>
                            Upload nutrition label images
                        </p>
                    </div>
                </Link>
                <Link to="/meal-planner" style={{ textDecoration: 'none' }}>
                    <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s', border: '2px solid #805ad5' }}
                        onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-4px)'}
                        onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
                        <div style={{ fontSize: '2.5rem', textAlign: 'center', marginBottom: '0.5rem' }}>🤖</div>
                        <h3 style={{ margin: '0 0 0.5rem 0', color: '#805ad5', textAlign: 'center' }}>AI Meal Planner</h3>
                        <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.9rem', textAlign: 'center' }}>
                            Generate personalized meal plans
                        </p>
                    </div>
                </Link>
            </div>

            {error && <p style={{ color: 'var(--accent)', marginBottom: '1rem' }}>{error}</p>}

            <div className="grid-cols-2" style={{ marginBottom: '2rem' }}>
                {/* Left Column: Charts */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

                    {/* Today's Summary */}
                    <div className="card">
                        <h3 style={{ marginTop: 0, color: 'var(--primary)', display: 'flex', justifyContent: 'space-between' }}>
                            <span>Today's Nutrition</span>
                            <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 'normal' }}>
                                Goal: {targetCalories} kcal
                            </span>
                        </h3>

                        {/* Progress Bar */}
                        <div style={{ width: '100%', height: '8px', backgroundColor: '#edf2f7', borderRadius: '4px', marginBottom: '1rem', marginTop: '0.5rem' }}>
                            <div style={{
                                width: `${caloriesProgress}%`,
                                height: '100%',
                                backgroundColor: caloriesProgress > 100 ? 'var(--accent)' : 'var(--primary)',
                                borderRadius: '4px',
                                transition: 'width 0.3s ease'
                            }}></div>
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                            <div style={{ textAlign: 'center', padding: '1rem', backgroundColor: 'var(--bg-hover)', borderRadius: 'var(--radius-sm)' }}>
                                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--primary)' }}>
                                    {totals.calories.toFixed(0)}
                                </div>
                                <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Calories Eaten</div>
                            </div>

                            {/* Pie Chart for Macros */}
                            <div style={{ width: '100%', height: 150 }}>
                                {activeMacroData.length > 0 ? (
                                    <ResponsiveContainer>
                                        <PieChart>
                                            <Pie
                                                data={activeMacroData}
                                                cx="50%"
                                                cy="50%"
                                                innerRadius={40}
                                                outerRadius={60}
                                                fill="#8884d8"
                                                paddingAngle={5}
                                                dataKey="value"
                                            >
                                                {activeMacroData.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                                ))}
                                            </Pie>
                                            <RechartsTooltip />
                                        </PieChart>
                                    </ResponsiveContainer>
                                ) : (
                                    <p style={{ textAlign: 'center', marginTop: '60px', color: '#888', fontSize: '0.8rem' }}>No data</p>
                                )}
                            </div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-around', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                            <span style={{ color: '#0088FE' }}>Protein: {totals.protein.toFixed(1)}g</span>
                            <span style={{ color: '#00C49F' }}>Carbs: {totals.carbs.toFixed(1)}g</span>
                            <span style={{ color: '#FFBB28' }}>Fat: {totals.fat.toFixed(1)}g</span>
                        </div>
                    </div>

                    {/* Weekly Trend */}
                    <div className="card">
                        <h3 style={{ marginTop: 0, color: 'var(--primary)' }}>Weekly Progress</h3>
                        <div style={{ width: '100%', height: 200 }}>
                            <ResponsiveContainer>
                                <LineChart data={weeklyStats}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="date" tickFormatter={(str) => new Date(str).toLocaleDateString(undefined, { weekday: 'short' })} />
                                    <YAxis />
                                    <RechartsTooltip />
                                    <Legend />
                                    <Line type="monotone" dataKey="calories" stroke="#8884d8" name="Calories" />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h3 style={{ marginTop: 0, color: 'var(--primary)' }}>Log a Meal</h3>
                    <MealForm onSuccess={fetchLogs} />
                </div>
            </div>

            <div className="card">
                <MealList logs={logs} onDelete={fetchLogs} />
            </div>

            {/* Voice Log Overlay */}
            {voiceResults && voiceResults.length > 0 && (
                <div style={{
                    position: 'fixed',
                    top: 0, left: 0, right: 0, bottom: 0,
                    backgroundColor: 'rgba(0,0,0,0.5)',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    zIndex: 200
                }}>
                    <div style={{
                        backgroundColor: 'var(--bg-card)',
                        padding: '2rem',
                        borderRadius: 'var(--radius-lg)',
                        maxWidth: '500px',
                        width: '90%',
                        maxHeight: '80vh',
                        overflowY: 'auto'
                    }}>
                        <h2 style={{ marginTop: 0 }}>🎙️ Confirm Voice Log</h2>
                        <p>We heard: found {voiceResults.length} items.</p>

                        <div style={{ display: 'grid', gap: '1rem' }}>
                            {voiceResults.map((item, idx) => (
                                <div key={idx} style={{
                                    padding: '1rem',
                                    border: '1px solid var(--border)',
                                    borderRadius: 'var(--radius-sm)',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center'
                                }}>
                                    <div>
                                        <strong>{item.name}</strong>
                                        <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                            {item.calories} kcal / 100g
                                            {item.match_found && <span style={{ marginLeft: '0.5rem', color: 'var(--secondary)' }}>(Found in DB)</span>}
                                        </div>
                                    </div>
                                    <button
                                        className="btn btn-primary btn-sm"
                                        onClick={() => confirmVoiceLog(item)}
                                    >
                                        Add
                                    </button>
                                </div>
                            ))}
                        </div>

                        <button
                            className="btn btn-secondary"
                            style={{ marginTop: '1.5rem', width: '100%' }}
                            onClick={() => setVoiceResults(null)}
                        >
                            Done
                        </button>
                    </div>
                </div>
            )}

            {/* Microphone FAB */}
            <button
                onClick={handleVoiceLog}
                style={{
                    position: 'fixed',
                    bottom: '2rem',
                    right: '2rem',
                    width: '64px',
                    height: '64px',
                    borderRadius: '50%',
                    backgroundColor: isListening ? '#e53e3e' : 'var(--primary)',
                    color: 'white',
                    border: 'none',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                    fontSize: '1.75rem',
                    cursor: 'pointer',
                    zIndex: 100,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'transform 0.2s, background-color 0.2s'
                }}
                title="Voice Log"
                onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
                onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
                {isListening ? '🛑' : '🎤'}
            </button>
        </div>
    );
};

export default Dashboard;
