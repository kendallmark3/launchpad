export function InsurancePanel({ bet, bankroll, onTakeInsurance, onDecline }) {
  const insuranceAmount = Math.floor(bet / 2);
  const canAfford = insuranceAmount <= bankroll;

  return (
    <div className="insurance-panel">
      <p>Dealer shows an Ace. Take insurance for {insuranceAmount}?</p>
      <div className="insurance-actions">
        <button type="button" onClick={() => onTakeInsurance(insuranceAmount)} disabled={!canAfford}>
          Insurance ({insuranceAmount})
        </button>
        <button type="button" className="primary" onClick={onDecline}>
          No thanks
        </button>
      </div>
    </div>
  );
}
