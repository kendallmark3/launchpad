const OUTCOME_LABEL = {
  win: "Win",
  loss: "Loss",
  push: "Push",
  blackjack: "Blackjack!",
};

export function ResultOverlay({ roundResult, onPlayAgain }) {
  if (!roundResult) return null;

  const netPayout = roundResult.handResults.reduce((sum, r) => sum + r.payout, 0) + roundResult.insurancePayout;

  return (
    <div className="result-overlay">
      <div className="result-card">
        {roundResult.handResults.map((result, i) => (
          <div key={i} className={`result-line result-${result.outcome}`}>
            {roundResult.handResults.length > 1 ? `Hand ${i + 1}: ` : ""}
            {OUTCOME_LABEL[result.outcome]} ({result.payout >= 0 ? "+" : ""}
            {result.payout})
          </div>
        ))}
        {roundResult.insurancePayout !== 0 && (
          <div className="result-line muted">
            Insurance: {roundResult.insurancePayout >= 0 ? "+" : ""}
            {roundResult.insurancePayout}
          </div>
        )}
        <div className="result-net">
          Net: {netPayout >= 0 ? "+" : ""}
          {netPayout}
        </div>
        <button type="button" className="primary" onClick={onPlayAgain}>
          Play Again
        </button>
      </div>
    </div>
  );
}
