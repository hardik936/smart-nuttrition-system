import React, { useState } from 'react';
import api from '../api/axios';
import RecommendationList from './RecommendationList';

const MealList = ({ logs }) => {
    const [selectedFoodId, setSelectedFoodId] = useState(null);

    const handleToggleRecs = (foodId) => {
        if (selectedFoodId === foodId) {
            setSelectedFoodId(null); // Close if already open
        } else {
            setSelectedFoodId(foodId);
        }
    };

    const handleDelete = async (logId) => {
        if (!window.confirm("Are you sure you want to delete this meal?")) return;
        try {
            await api.delete(`/api/v1/logs/${logId}`);
            if (window.location.reload) window.location.reload(); // Simple refresh for now
        } catch (err) {
            console.error("Failed to delete log", err);
            alert("Failed to delete meal.");
        }
    };

    const handleEdit = async (log) => {
        const newQuantity = prompt("Enter new quantity (g):", log.quantity);
        if (newQuantity && !isNaN(newQuantity)) {
            try {
                await api.put(`/api/v1/logs/${log.id}?quantity=${newQuantity}`);
                if (window.location.reload) window.location.reload();
            } catch (err) {
                console.error("Failed to update log", err);
                alert("Failed to update meal.");
            }
        }
    };

    if (!logs || logs.length === 0) {
        return <p>No meals logged yet.</p>;
    }

    return (

        <div style={{ marginTop: '0.5rem' }}>
            <h3 style={{ color: 'var(--text-primary)', marginBottom: '1rem' }}>Recent Meals</h3>
            <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: '0' }}>
                    <thead>
                        <tr style={{ textAlign: 'left', color: 'var(--text-secondary)' }}>
                            <th style={{ padding: '1rem', borderBottom: '2px solid var(--border)' }}>Date</th>
                            <th style={{ padding: '1rem', borderBottom: '2px solid var(--border)' }}>Food</th>
                            <th style={{ padding: '1rem', borderBottom: '2px solid var(--border)' }}>Qty</th>
                            <th style={{ padding: '1rem', borderBottom: '2px solid var(--border)' }}>Calories</th>
                            <th style={{ padding: '1rem', borderBottom: '2px solid var(--border)' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs.map((log) => (
                            <React.Fragment key={log.id}>
                                <tr style={{ backgroundColor: selectedFoodId === log.food?.id ? 'var(--bg-hover)' : 'transparent', transition: 'background-color 0.2s' }}>
                                    <td style={{ padding: '1rem', borderBottom: '1px solid var(--border)' }}>{new Date(log.timestamp).toLocaleDateString()}</td>
                                    <td style={{ padding: '1rem', borderBottom: '1px solid var(--border)', fontWeight: '500' }}>{log.food ? log.food.name : 'Unknown Food'}</td>
                                    <td style={{ padding: '1rem', borderBottom: '1px solid var(--border)' }}>{log.quantity}g</td>
                                    <td style={{ padding: '1rem', borderBottom: '1px solid var(--border)' }}>
                                        {log.food ? ((log.food.calories / 100) * log.quantity).toFixed(0) : '-'}
                                    </td>
                                    <td style={{ padding: '1rem', borderBottom: '1px solid var(--border)' }}>
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            <button
                                                onClick={() => handleEdit(log)}
                                                className="btn btn-sm"
                                                style={{ backgroundColor: '#f0ad4e', color: 'white', border: 'none' }}
                                            >
                                                Edit
                                            </button>
                                            <button
                                                onClick={() => handleDelete(log.id)}
                                                className="btn btn-sm"
                                                style={{ backgroundColor: '#d9534f', color: 'white', border: 'none' }}
                                            >
                                                Delete
                                            </button>
                                            {log.food && (
                                                <button
                                                    onClick={() => handleToggleRecs(log.food.id)}
                                                    className="btn btn-sm btn-secondary"
                                                >
                                                    {selectedFoodId === log.food.id ? 'Hide Recs' : 'Similar'}
                                                </button>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                                {selectedFoodId === log.food?.id && (
                                    <tr>
                                        <td colSpan="5" style={{ padding: '0 1rem 1rem 1rem', borderBottom: '1px solid var(--border)' }}>
                                            <RecommendationList
                                                foodId={selectedFoodId}
                                                onClose={() => setSelectedFoodId(null)}
                                            />
                                        </td>
                                    </tr>
                                )}
                            </React.Fragment>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default MealList;
