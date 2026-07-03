export function StatsPanel({ stats, hintEnabled, onToggleHint, onReset }) {
  const winRate = stats.handsPlayed === 0 ? 0 : Math.round((stats.wins / stats.handsPlayed) * 100);

  return (
    <div className="stats-panel">
      <div className="stats-grid">
        <div>
          <span className="stat-value">{stats.handsPlayed}</span>
          <span className="stat-label">Hands</span>
        </div>
        <div>
          <span className="stat-value">{winRate}%</span>
          <span className="stat-label">Win rate</span>
        </div>
        <div>
          <span className="stat-value">{stats.currentStreak}</span>
          <span className="stat-label">Streak</span>
        </div>
        <div>
          <span className="stat-value">{stats.biggestWin}</span>
          <span className="stat-label">Biggest win</span>
        </div>
      </div>
      <label className="hint-toggle">
        <input type="checkbox" checked={hintEnabled} onChange={(e) => onToggleHint(e.target.checked)} />
        Strategy hint
      </label>
      <button type="button" className="reset-button" onClick={onReset}>
        Reset bankroll &amp; stats
      </button>
    </div>
  );
}
