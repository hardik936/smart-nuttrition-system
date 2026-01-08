import React from 'react';

const Gamification = ({ streak, logs, targetCalories, totalCalories }) => {
    // Determine Badges
    const badges = [];

    // Badge 1: Early Bird (Logged Breakfast - approximate time or meal name check)
    // Simplified: Logged any meal before 10 AM (assuming UTC/Local conversion)
    // Ideally we check log timestamps. For MVP let's check if we have > 0 logs.
    if (logs.length > 0) {
        badges.push({ icon: '🌅', label: 'Started Strong', desc: 'Logged first meal' });
    }

    // Badge 2: On Track (Within 10% of calorie goal)
    if (totalCalories > 0 && Math.abs(totalCalories - targetCalories) < (targetCalories * 0.1)) {
        badges.push({ icon: '🎯', label: 'On Target', desc: 'Close to calorie goal' });
    }

    // Badge 3: Protein Champ (If protein > 100g - hardcoded for MVP or based on 30% ratio)
    // Need access to total protein. For now, let's just use Streak > 3.
    if (streak >= 3) {
        badges.push({ icon: '🔥', label: 'On Fire', desc: '3+ Day Streak' });
    }

    if (badges.length === 0 && streak === 0) return null;

    return (
        <div className="card" style={{ background: 'linear-gradient(135deg, #1E7F5A 0%, #4FB6A3 100%)', color: 'white', border: 'none' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h2 style={{ color: 'white', marginBottom: '0.2rem' }}>
                        🔥 {streak} Day Streak
                    </h2>
                    <p style={{ margin: 0, opacity: 0.9 }}>
                        Keep logging to maintain your fire!
                    </p>
                </div>
                {badges.length > 0 && (
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                        {badges.map((b, i) => (
                            <div key={i} title={b.desc} style={{
                                backgroundColor: 'rgba(255,255,255,0.2)',
                                padding: '0.5rem',
                                borderRadius: '8px',
                                textAlign: 'center',
                                cursor: 'help'
                            }}>
                                <div style={{ fontSize: '1.5rem' }}>{b.icon}</div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Gamification;
