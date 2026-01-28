import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

const Profile = () => {
    const { user, login } = useAuth();
    const [formData, setFormData] = useState({
        age: '',
        weight: '',
        height: '',
        activity_level: 'sedentary',
        goal: 'maintain',
        target_calories: 2000,
        is_public: true
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const res = await api.get('/auth/me');
            const data = res.data;
            setFormData({
                age: data.age || '',
                weight: data.weight || '',
                height: data.height || '',
                activity_level: data.activity_level || 'sedentary',
                goal: data.goal || 'maintain',
                target_calories: data.target_calories || 2000,
                is_public: data.is_public !== undefined ? data.is_public : true
            });
            setLoading(false);
        } catch (err) {
            console.error(err);
            setMessage('Failed to load profile.');
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => {
            const newData = { ...prev, [name]: value };
            // Auto-calculate suggested calories if physical stats change
            if (['age', 'weight', 'height', 'activity_level', 'goal'].includes(name)) {
                const suggested = calculateCalories({ ...newData, [name]: value });
                if (suggested) newData.target_calories = suggested;
            }
            return newData;
        });
    };

    const calculateCalories = (data) => {
        const w = parseFloat(data.weight);
        const h = parseFloat(data.height);
        const a = parseFloat(data.age);

        if (!w || !h || !a) return null;

        // BMR (Mifflin-St Jeor)
        let bmr = (10 * w) + (6.25 * h) - (5 * a) + 5;

        // TDEE Multipliers
        const multipliers = {
            sedentary: 1.2,
            light: 1.375,
            moderate: 1.55,
            active: 1.725
        };

        let tdee = bmr * (multipliers[data.activity_level] || 1.2);

        if (data.goal === 'lose_weight') return Math.round(tdee - 500);
        if (data.goal === 'gain_muscle') return Math.round(tdee + 300);
        return Math.round(tdee);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setMessage('');
        try {
            await api.put('/auth/me', {
                age: parseInt(formData.age) || null,
                weight: parseFloat(formData.weight) || null,
                height: parseFloat(formData.height) || null,
                activity_level: formData.activity_level,
                goal: formData.goal,
                target_calories: parseInt(formData.target_calories),
                is_public: formData.is_public
            });
            setMessage('Profile updated successfully!');
        } catch (err) {
            console.error(err);
            setMessage('Failed to update profile.');
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="container">
            <h1>My Profile</h1>
            {message && <p style={{ color: message.includes('Success') ? 'green' : 'red' }}>{message}</p>}

            <div className="card">
                <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1rem', maxWidth: '500px' }}>
                    <div className="form-group">
                        <label>Age</label>
                        <input type="number" name="age" className="input-field" value={formData.age} onChange={handleChange} />
                    </div>
                    <div className="form-group">
                        <label>Weight (kg)</label>
                        <input type="number" name="weight" className="input-field" value={formData.weight} onChange={handleChange} />
                    </div>
                    <div className="form-group">
                        <label>Height (cm)</label>
                        <input type="number" name="height" className="input-field" value={formData.height} onChange={handleChange} />
                    </div>

                    <div className="form-group">
                        <label>Activity Level</label>
                        <select name="activity_level" className="input-field" value={formData.activity_level} onChange={handleChange}>
                            <option value="sedentary">Sedentary (Office job)</option>
                            <option value="light">Lightly Active (1-3 days/week)</option>
                            <option value="moderate">Moderately Active (3-5 days/week)</option>
                            <option value="active">Active (6-7 days/week)</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Goal</label>
                        <select name="goal" className="input-field" value={formData.goal} onChange={handleChange}>
                            <option value="lose_weight">Lose Weight</option>
                            <option value="maintain">Maintain Weight</option>
                            <option value="gain_muscle">Gain Muscle</option>
                        </select>
                    </div>

                    <div style={{ borderTop: '1px solid #eee', paddingTop: '1rem', marginTop: '0.5rem' }}>
                        <div className="form-group" style={{ flexDirection: 'row', alignItems: 'center', gap: '0.5rem' }}>
                            <input
                                type="checkbox"
                                name="is_public"
                                id="is_public"
                                checked={formData.is_public === undefined ? true : formData.is_public}
                                onChange={(e) => setFormData(prev => ({ ...prev, is_public: e.target.checked }))}
                            />
                            <label htmlFor="is_public" style={{ margin: 0 }}>Public Profile (Visible on Leaderboard)</label>
                        </div>
                    </div>

                    <div style={{ borderTop: '1px solid #eee', paddingTop: '1rem', marginTop: '0.5rem' }}>
                        <div className="form-group">
                            <label style={{ fontWeight: 'bold', color: 'var(--primary)' }}>Target Daily Calories</label>
                            <input type="number" name="target_calories" className="input-field" value={formData.target_calories} onChange={handleChange} />
                            <small style={{ color: '#718096' }}> Auto-calculated based on your stats. You can manually override.</small>
                        </div>
                    </div>

                    <button type="submit" className="btn btn-primary" disabled={saving}>
                        {saving ? 'Saving...' : 'Save Profile'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Profile;
