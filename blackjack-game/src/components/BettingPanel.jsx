const CHIP_VALUES = [5, 25, 100, 500];

export function BettingPanel({ bankroll, bet, onAddChip, onClearBet, onDeal }) {
  return (
    <div className="betting-panel">
      <div className="bet-display">
        Bet: <strong>{bet}</strong> <span className="muted">/ Bankroll: {bankroll}</span>
      </div>
      <div className="chip-row">
        {CHIP_VALUES.map((value) => (
          <button
            key={value}
            type="button"
            className={`chip chip-${value}`}
            onClick={() => onAddChip(value)}
            disabled={bet + value > bankroll}
          >
            {value}
          </button>
        ))}
      </div>
      <div className="betting-actions">
        <button type="button" onClick={onClearBet} disabled={bet === 0}>
          Clear
        </button>
        <button type="button" className="primary" onClick={onDeal} disabled={bet === 0}>
          Deal
        </button>
      </div>
    </div>
  );
}
