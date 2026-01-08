import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Html5QrcodeScanner } from 'html5-qrcode';
import '../index.css';
import api from '../api/axios'; // Use configured api instance

function ScanLabel() {
    const navigate = useNavigate();
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [nutritionData, setNutritionData] = useState(null);
    const [foodName, setFoodName] = useState('');
    const [quantity, setQuantity] = useState(100);
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);
    const [scanMode, setScanMode] = useState('image'); // 'image' or 'barcode'

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file && (file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/webp')) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setError(null);
            setNutritionData(null);
            setFoodName('');
            setQuantity(100);
        } else {
            setError('Please select a valid image file (JPEG, PNG, or WebP)');
        }
    };

    const handleScan = async () => {
        if (!selectedFile) {
            setError('Please select an image first');
            return;
        }

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await api.post('/api/v1/ocr/scan', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setNutritionData(response.data);
            if (response.data.name_guess) {
                setFoodName(response.data.name_guess);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to scan label. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async (e) => {
        e.preventDefault();
        if (!foodName || !nutritionData) return;

        setSaving(true);
        setError(null);

        try {
            // 1. Create Food
            const foodRes = await api.post('/api/v1/foods/', {
                name: foodName,
                ...nutritionData
            });

            const foodId = foodRes.data.id;

            // 2. Log Food (using entered quantity)
            await api.post('/api/v1/logs/', {
                food_id: foodId,
                quantity: parseFloat(quantity)
            });

            // 3. Redirect
            navigate('/dashboard');

        } catch (err) {
            console.error(err);
            const detail = err.response?.data?.detail;
            setError(detail ? `Error: ${JSON.stringify(detail)}` : 'Failed to save food and log it.');
        } finally {
            setSaving(false);
        }
    };

    useEffect(() => {
        if (scanMode === 'barcode' && !nutritionData) {
            const scanner = new Html5QrcodeScanner(
                "reader",
                { fps: 10, qrbox: 250 },
                /* verbose= */ false
            );

            scanner.render(onScanSuccess, onScanFailure);

            async function onScanSuccess(decodedText) {
                // Handle the scanned code as you like, for example:
                console.log(`Code matched = ${decodedText}`);
                scanner.clear();
                setLoading(true);
                try {
                    const res = await api.get(`/api/v1/foods/barcode/${decodedText}`);
                    setNutritionData(res.data);
                    setFoodName(res.data.name);
                    setError(null);
                } catch (err) {
                    setError('Product not found in OpenFoodFacts database.');
                } finally {
                    setLoading(false);
                }
            }

            function onScanFailure(error) {
                // handle scan failure, usually better to ignore and keep scanning.
                // console.warn(`Code scan error = ${error}`);
            }

            return () => {
                scanner.clear().catch(error => console.error("Failed to clear html5-qrcode scanner. ", error));
            };
        }
    }, [scanMode, nutritionData]);

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
            <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>
                📸 Scan & Log
            </h1>

            {!nutritionData && (
                <div style={{ display: 'flex', marginBottom: '1.5rem', borderBottom: '1px solid #e2e8f0' }}>
                    <button
                        onClick={() => setScanMode('image')}
                        style={{
                            padding: '1rem',
                            borderBottom: scanMode === 'image' ? '2px solid #48bb78' : 'none',
                            fontWeight: scanMode === 'image' ? 'bold' : 'normal',
                            color: scanMode === 'image' ? '#2f855a' : '#718096',
                            background: 'none',
                            border: 'none',
                            borderBottom: scanMode === 'image' ? '2px solid #48bb78' : 'none',
                            cursor: 'pointer',
                            flex: 1
                        }}
                    >
                        📷 Scan Image
                    </button>
                    <button
                        onClick={() => setScanMode('barcode')}
                        style={{
                            padding: '1rem',
                            borderBottom: scanMode === 'barcode' ? '2px solid #48bb78' : 'none',
                            fontWeight: scanMode === 'barcode' ? 'bold' : 'normal',
                            color: scanMode === 'barcode' ? '#2f855a' : '#718096',
                            background: 'none',
                            border: 'none',
                            borderBottom: scanMode === 'barcode' ? '2px solid #48bb78' : 'none',
                            cursor: 'pointer',
                            flex: 1
                        }}
                    >
                        ║▌ Scan Barcode
                    </button>
                </div>
            )}

            {!nutritionData ? (
                <>
                    {scanMode === 'image' ? (
                        <div style={{
                            border: '2px dashed #cbd5e0',
                            borderRadius: '8px',
                            padding: '2rem',
                            textAlign: 'center',
                            marginBottom: '1.5rem',
                            backgroundColor: '#f7fafc'
                        }}>
                            <input
                                type="file"
                                accept="image/jpeg,image/png,image/webp"
                                onChange={handleFileSelect}
                                style={{ display: 'none' }}
                                id="file-upload"
                            />
                            <label
                                htmlFor="file-upload"
                                style={{
                                    cursor: 'pointer',
                                    padding: '0.75rem 1.5rem',
                                    backgroundColor: '#4299e1',
                                    color: 'white',
                                    borderRadius: '6px',
                                    display: 'inline-block',
                                    fontWeight: '500'
                                }}
                            >
                                Choose Image
                            </label>
                            <p style={{ marginTop: '0.5rem', color: '#718096', fontSize: '0.875rem' }}>
                                Supports JPEG and PNG
                            </p>
                        </div>
                    ) : (
                        <div style={{
                            marginBottom: '1.5rem',
                            backgroundColor: '#f7fafc',
                            padding: '1rem',
                            borderRadius: '8px',
                            textAlign: 'center'
                        }}>
                            <div id="reader" style={{ width: '100%' }}></div>
                            <p style={{ marginTop: '1rem', color: '#718096' }}>Point your camera at a food barcode</p>
                        </div>
                    )}

                    {preview && scanMode === 'image' && (
                        <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
                            <img
                                src={preview}
                                alt="Preview"
                                style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
                            />
                        </div>
                    )}

                    {selectedFile && scanMode === 'image' && (
                        <button
                            onClick={handleScan}
                            disabled={loading}
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                backgroundColor: loading ? '#a0aec0' : '#48bb78',
                                color: 'white',
                                border: 'none',
                                borderRadius: '6px',
                                fontSize: '1rem',
                                fontWeight: '600',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                marginBottom: '1.5rem'
                            }}
                        >
                            {loading ? 'Scanning...' : '🔍 Scan Label'}
                        </button>
                    )}
                </>
            ) : (
                <div className="card">
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#2f855a' }}>
                        ✅ Nutrition Extracted
                    </h2>

                    <form onSubmit={handleSave}>
                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Food Name</label>
                            <input
                                type="text"
                                value={foodName}
                                onChange={(e) => setFoodName(e.target.value)}
                                placeholder="e.g., My Protein Bar"
                                required
                                style={{ width: '100%', padding: '0.5rem', fontSize: '1rem' }}
                            />
                        </div>

                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Quantity Consumed (g)</label>
                            <input
                                type="number"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                                placeholder="e.g., 100"
                                required
                                style={{ width: '100%', padding: '0.5rem', fontSize: '1rem' }}
                            />
                        </div>

                        <div className="nutrition-grid">
                            <div>
                                <label style={{ display: 'block', fontSize: '0.9rem', color: '#718096' }}>Calories (kcal / 100g)</label>
                                <input
                                    type="number"
                                    value={nutritionData.calories}
                                    onChange={(e) => setNutritionData({ ...nutritionData, calories: parseFloat(e.target.value) })}
                                    style={{ width: '100%', padding: '0.5rem', border: '1px solid #e2e8f0', borderRadius: '4px' }}
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', fontSize: '0.9rem', color: '#718096' }}>Protein (g / 100g)</label>
                                <input
                                    type="number"
                                    value={nutritionData.protein}
                                    onChange={(e) => setNutritionData({ ...nutritionData, protein: parseFloat(e.target.value) })}
                                    style={{ width: '100%', padding: '0.5rem', border: '1px solid #e2e8f0', borderRadius: '4px' }}
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', fontSize: '0.9rem', color: '#718096' }}>Carbs (g / 100g)</label>
                                <input
                                    type="number"
                                    value={nutritionData.carbs}
                                    onChange={(e) => setNutritionData({ ...nutritionData, carbs: parseFloat(e.target.value) })}
                                    style={{ width: '100%', padding: '0.5rem', border: '1px solid #e2e8f0', borderRadius: '4px' }}
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', fontSize: '0.9rem', color: '#718096' }}>Fat (g / 100g)</label>
                                <input
                                    type="number"
                                    value={nutritionData.fat}
                                    onChange={(e) => setNutritionData({ ...nutritionData, fat: parseFloat(e.target.value) })}
                                    style={{ width: '100%', padding: '0.5rem', border: '1px solid #e2e8f0', borderRadius: '4px' }}
                                />
                            </div>
                        </div>

                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <button
                                type="button"
                                onClick={() => setNutritionData(null)}
                                style={{
                                    flex: 1,
                                    padding: '0.75rem',
                                    backgroundColor: '#e2e8f0',
                                    color: '#4a5568',
                                    border: 'none',
                                    borderRadius: '6px',
                                    fontWeight: '600',
                                    cursor: 'pointer'
                                }}
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={saving}
                                style={{
                                    flex: 1,
                                    padding: '0.75rem',
                                    backgroundColor: '#48bb78',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '6px',
                                    fontWeight: '600',
                                    cursor: saving ? 'not-allowed' : 'pointer'
                                }}
                            >
                                {saving ? 'Saving...' : '💾 Save & Log'}
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {error && (
                <div style={{
                    padding: '1rem',
                    backgroundColor: '#fed7d7',
                    color: '#c53030',
                    borderRadius: '6px',
                    marginBottom: '1.5rem',
                    marginTop: '1rem'
                }}>
                    {error}
                </div>
            )}
        </div>
    );
}

export default ScanLabel;
