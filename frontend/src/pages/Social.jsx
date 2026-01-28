import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

const Social = () => {
    const { user } = useAuth();
    const [activeTab, setActiveTab] = useState('leaderboard');
    const [leaderboard, setLeaderboard] = useState([]);
    const [friends, setFriends] = useState([]);
    const [searchResults, setSearchResults] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(false);

    const fetchLeaderboard = async () => {
        setLoading(true);
        try {
            const res = await api.get('/api/v1/social/leaderboard');
            setLeaderboard(res.data);
        } catch (err) {
            console.error("Failed to fetch leaderboard", err);
        } finally {
            setLoading(false);
        }
    };

    const fetchFriends = async () => {
        setLoading(true);
        try {
            const res = await api.get('/api/v1/social/friends');
            setFriends(res.data);
        } catch (err) {
            console.error("Failed to fetch friends", err);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;

        try {
            const res = await api.get(`/api/v1/social/users/search?query=${searchQuery}`);
            setSearchResults(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const followUser = async (userId) => {
        try {
            await api.post(`/api/v1/social/follow/${userId}`);
            // Refresh logic
            if (activeTab === 'friends') fetchFriends();
            if (searchResults.length > 0) {
                setSearchResults(prev => prev.map(u => u.id === userId ? { ...u, is_following: true } : u));
            }
        } catch (err) {
            alert(err.response?.data?.detail || "Failed to follow user");
        }
    };

    const unfollowUser = async (userId) => {
        if (!window.confirm("Are you sure?")) return;
        try {
            await api.delete(`/api/v1/social/unfollow/${userId}`);
            if (activeTab === 'friends') setFriends(prev => prev.filter(f => f.id !== userId));
        } catch (err) {
            alert("Failed to unfollow");
        }
    };

    useEffect(() => {
        if (activeTab === 'leaderboard') fetchLeaderboard();
        if (activeTab === 'friends') fetchFriends();
    }, [activeTab]);

    return (
        <div className="container">
            <h1 style={{ marginBottom: '1.5rem' }}>🏆 Social Hub</h1>

            <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
                <button
                    className={`btn ${activeTab === 'leaderboard' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveTab('leaderboard')}
                >
                    Global Leaderboard
                </button>
                <button
                    className={`btn ${activeTab === 'friends' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveTab('friends')}
                >
                    Friends & Search
                </button>
            </div>

            {loading && <p>Loading...</p>}

            {activeTab === 'leaderboard' && (
                <div className="card">
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ borderBottom: '2px solid var(--border)', textAlign: 'left' }}>
                                <th style={{ padding: '1rem' }}>Rank</th>
                                <th style={{ padding: '1rem' }}>User</th>
                                <th style={{ padding: '1rem' }}>Streak 🔥</th>
                            </tr>
                        </thead>
                        <tbody>
                            {leaderboard.map((entry, index) => (
                                <tr key={entry.id} style={{
                                    backgroundColor: entry.is_me ? 'var(--bg-hover)' : 'transparent',
                                    borderBottom: '1px solid var(--border)'
                                }}>
                                    <td style={{ padding: '1rem', fontWeight: 'bold' }}>#{index + 1}</td>
                                    <td style={{ padding: '1rem' }}>
                                        {entry.email.split('@')[0]}
                                        {entry.is_me && " (You)"}
                                    </td>
                                    <td style={{ padding: '1rem' }}>{entry.streak_count}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {activeTab === 'friends' && (
                <div>
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <h3>Find Friends</h3>
                        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem' }}>
                            <input
                                type="text"
                                placeholder="Search by email..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                style={{ flex: 1, padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border)' }}
                            />
                            <button type="submit" className="btn btn-primary">Search</button>
                        </form>

                        {searchResults.length > 0 && (
                            <div style={{ marginTop: '1rem', display: 'grid', gap: '0.5rem' }}>
                                {searchResults.map(user => (
                                    <div key={user.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.5rem', backgroundColor: 'var(--bg)', borderRadius: '4px' }}>
                                        <span>{user.email}</span>
                                        {user.is_following ? (
                                            <span style={{ color: 'var(--primary)' }}>Following</span>
                                        ) : (
                                            <button className="btn btn-sm btn-primary" onClick={() => followUser(user.id)}>Follow</button>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="card">
                        <h3>Your Friends</h3>
                        {friends.length === 0 ? <p>You haven't followed anyone yet.</p> : (
                            <div style={{ display: 'grid', gap: '1rem' }}>
                                {friends.map(friend => (
                                    <div key={friend.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', border: '1px solid var(--border)', borderRadius: '8px' }}>
                                        <div>
                                            <strong>{friend.email}</strong>
                                            <div>Streak: {friend.streak_count} 🔥</div>
                                        </div>
                                        <button className="btn btn-sm btn-secondary" onClick={() => unfollowUser(friend.id)}>Unfollow</button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Social;
