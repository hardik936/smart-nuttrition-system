import React, { useState, useEffect } from 'react';
import api from '../api/axios';

const RecommendationList = ({ foodId, onClose }) => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchRecommendations = async () => {
            setLoading(true);
            try {
                const response = await api.get(`/recommend/${foodId}`);
                setRecommendations(response.data);
                setLoading(false);
            } catch (err) {
                console.error(err);
                setError('Failed to load recommendations.');
                setLoading(false);
            }
        };

        if (foodId) {
            fetchRecommendations();
        }
    }, [foodId]);

    return (
        <div style={{ padding: '10px', backgroundColor: '#eef', border: '1px solid #ccd', marginTop: '10px', borderRadius: '5px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <h4 style={{ margin: 0 }}>Similar Foods</h4>
                <button onClick={onClose} style={{ cursor: 'pointer', padding: '2px 5px' }}>Close</button>
            </div>

            {loading && <p>Finding similar foods...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && recommendations.length === 0 && <p>No recommendations found.</p>}

            {!loading && !error && recommendations.length > 0 && (
                <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                    {recommendations.map(item => (
                        <li key={item.id} style={{ padding: '5px 0', borderBottom: '1px solid #ddd', fontSize: '0.9em' }}>
                            <strong>{item.name}</strong> - {item.calories.toFixed(0)} kcal
                            <br />
                            <span style={{ color: '#666', fontSize: '0.85em' }}>
                                P: {item.protein}g | C: {item.carbs}g | F: {item.fat}g
                            </span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default RecommendationList;
