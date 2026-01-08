import React, { useState } from 'react';
import api from '../api/axios';
import FoodSearch from './FoodSearch';

const MealForm = ({ onSuccess }) => {
    const [selectedFood, setSelectedFood] = useState(null);
    const [quantity, setQuantity] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!selectedFood) {
            setError('Please select a food item');
            return;
        }

        try {
            await api.post('/api/v1/logs/', {
                food_id: selectedFood.id,
                quantity: parseFloat(quantity)
            });
            // Reset form
            setSelectedFood(null);
            setQuantity('');
            // Notify parent to refresh list
            if (onSuccess) onSuccess();
        } catch (err) {
            console.error(err);
            let msg = err.response?.data?.detail || 'Failed to log meal. Please check your input.';
            if (err.response?.status === 401) {
                msg = "Session expired. Please logout and login again.";
            }
            setError(msg);
        }
    };

    return (

        <div>
            {error && <p style={{ color: 'var(--accent)', fontSize: '0.9rem', marginBottom: '1rem' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Search Food</label>
                    <FoodSearch
                        onSelect={setSelectedFood}
                        value={selectedFood}
                    />
                </div>
                <div className="form-group">
                    <label>Quantity (g)</label>
                    <input
                        type="number"
                        step="1"
                        min="1"
                        className="input-field"
                        placeholder="E.g. 100"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
                    Add Meal
                </button>
            </form>
        </div>
    );
};

export default MealForm;
