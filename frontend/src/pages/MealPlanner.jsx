import React, { useState } from 'react';
import axios from 'axios';
import '../index.css';

function MealPlanner() {
    const [formData, setFormData] = useState({
        calories: 2000,
        diet: 'Balanced',
        allergies: ''
    });
    const [mealPlan, setMealPlan] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setMealPlan(null);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/plan/generate-plan', formData);
            setMealPlan(response.data.plan);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate meal plan. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleCommit = async () => {
        if (!mealPlan) return;
        setLoading(true);
        try {
            await axios.post('http://127.0.0.1:8000/api/v1/plan/commit', { plan: mealPlan });
            alert('Meal plan added to your log!');
        } catch (err) {
            alert('Failed to add meal plan.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
            <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>
                🤖 AI Meal Planner
            </h1>

            <form onSubmit={handleSubmit} style={{
                backgroundColor: '#f7fafc',
                padding: '2rem',
                borderRadius: '8px',
                marginBottom: '2rem',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', fontWeight: '600', marginBottom: '0.5rem', color: '#2d3748' }}>
                        Target Calories
                    </label>
                    <input
                        type="number"
                        name="calories"
                        value={formData.calories}
                        onChange={handleChange}
                        min="1000"
                        max="5000"
                        style={{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #cbd5e0',
                            borderRadius: '6px',
                            fontSize: '1rem'
                        }}
                    />
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', fontWeight: '600', marginBottom: '0.5rem', color: '#2d3748' }}>
                        Diet Type
                    </label>
                    <select
                        name="diet"
                        value={formData.diet}
                        onChange={handleChange}
                        style={{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #cbd5e0',
                            borderRadius: '6px',
                            fontSize: '1rem'
                        }}
                    >
                        <option value="Balanced">Balanced</option>
                        <option value="High Protein">High Protein</option>
                        <option value="Low Carb">Low Carb</option>
                        <option value="Vegetarian">Vegetarian</option>
                        <option value="Vegan">Vegan</option>
                        <option value="Keto">Keto</option>
                    </select>
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', fontWeight: '600', marginBottom: '0.5rem', color: '#2d3748' }}>
                        Allergies (Optional)
                    </label>
                    <input
                        type="text"
                        name="allergies"
                        value={formData.allergies}
                        onChange={handleChange}
                        placeholder="e.g., Peanuts, Dairy"
                        style={{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #cbd5e0',
                            borderRadius: '6px',
                            fontSize: '1rem'
                        }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="btn btn-primary"
                    style={{
                        width: '100%',
                        padding: '0.75rem',
                        backgroundColor: loading ? '#a0aec0' : '#805ad5',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        fontSize: '1rem',
                        fontWeight: '600',
                        cursor: loading ? 'not-allowed' : 'pointer'
                    }}
                >
                    {loading ? 'Generating...' : '✨ Generate Meal Plan'}
                </button>
            </form>

            {error && (
                <div style={{
                    padding: '1rem',
                    backgroundColor: '#fed7d7',
                    color: '#c53030',
                    borderRadius: '6px',
                    marginBottom: '1.5rem'
                }}>
                    {error}
                </div>
            )}

            {mealPlan && (
                <div style={{
                    padding: '2rem',
                    backgroundColor: '#faf5ff',
                    border: '1px solid #d6bcfa',
                    borderRadius: '8px'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#6b46c1', margin: 0 }}>
                            🍽️ Your Personalized Meal Plan
                        </h2>
                        {Array.isArray(mealPlan) && (
                            <button
                                onClick={handleCommit}
                                disabled={loading}
                                style={{
                                    backgroundColor: '#48bb78',
                                    color: 'white',
                                    border: 'none',
                                    padding: '0.5rem 1rem',
                                    borderRadius: '6px',
                                    fontWeight: 'bold',
                                    cursor: 'pointer'
                                }}
                            >
                                ✅ Eat This Plan
                            </button>
                        )}
                    </div>

                    {Array.isArray(mealPlan) ? (
                        <div style={{ display: 'grid', gap: '1rem' }}>
                            {mealPlan.map((item, index) => (
                                <div key={index} style={{
                                    backgroundColor: 'white',
                                    padding: '1rem',
                                    borderRadius: '6px',
                                    borderLeft: '4px solid #805ad5',
                                    boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
                                }}>
                                    <div style={{ fontWeight: 'bold', color: '#553c9a', fontSize: '0.9rem' }}>{item.meal}</div>
                                    <div style={{ fontSize: '1.1rem', color: '#2d3748' }}>{item.food}</div>
                                    {item.calories && (
                                        <div style={{ fontSize: '0.9rem', color: '#718096' }}>~{item.calories} kcal</div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.8', color: '#2d3748' }}>
                            {typeof mealPlan === 'string' ? mealPlan : JSON.stringify(mealPlan, null, 2)}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default MealPlanner;
