import React, { useState, useEffect } from 'react';
import api from '../api/axios';

function FoodSearch({ onSelect, value }) {
    const [query, setQuery] = useState('');
    const [foods, setFoods] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const searchFoods = async () => {
            if (query.length === 0) {
                // Load all foods when empty
                setLoading(true);
                try {
                    const response = await api.get('/api/v1/foods/search');
                    setFoods(response.data);
                } catch (err) {
                    console.error('Error fetching foods:', err);
                } finally {
                    setLoading(false);
                }
                return;
            }

            // Debounce search
            const timer = setTimeout(async () => {
                setLoading(true);
                try {
                    const response = await api.get(`/api/v1/foods/search?q=${query}`);
                    setFoods(response.data);
                } catch (err) {
                    console.error('Error searching foods:', err);
                } finally {
                    setLoading(false);
                }
            }, 300);

            return () => clearTimeout(timer);
        };

        searchFoods();
    }, [query]);

    const handleSelect = (food) => {
        onSelect(food);
        setQuery(food.name);
        setShowDropdown(false);
    };

    return (
        <div style={{ position: 'relative' }}>
            <input
                type="text"
                className="input-field"
                placeholder="Search for food..."
                value={query}
                onChange={(e) => {
                    setQuery(e.target.value);
                    setShowDropdown(true);
                }}
                onFocus={() => setShowDropdown(true)}
                style={{ width: '100%' }}
            />

            {showDropdown && foods.length > 0 && (
                <div style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    right: 0,
                    backgroundColor: 'white',
                    border: '1px solid #cbd5e0',
                    borderRadius: '6px',
                    marginTop: '4px',
                    maxHeight: '300px',
                    overflowY: 'auto',
                    zIndex: 1000,
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                }}>
                    {loading && (
                        <div style={{ padding: '0.75rem', color: '#718096' }}>
                            Searching...
                        </div>
                    )}
                    {!loading && foods.map((food) => (
                        <div
                            key={food.id}
                            onClick={() => handleSelect(food)}
                            style={{
                                padding: '0.75rem',
                                cursor: 'pointer',
                                borderBottom: '1px solid #e2e8f0',
                                transition: 'background-color 0.2s'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f7fafc'}
                            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'white'}
                        >
                            <div style={{ fontWeight: '600', color: '#2d3748' }}>{food.name}</div>
                            <div style={{ fontSize: '0.875rem', color: '#718096' }}>
                                {food.calories} cal | P: {food.protein}g | C: {food.carbs}g | F: {food.fat}g
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default FoodSearch;
