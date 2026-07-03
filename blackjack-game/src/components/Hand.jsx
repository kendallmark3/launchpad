import { Card } from "./Card.jsx";
import { evaluateHand } from "../engine/hand.js";

export function Hand({ cards, hideSecondCard = false, label, active = false, bet }) {
  const visibleCards = hideSecondCard ? [cards[0]] : cards;
  const evalResult = hideSecondCard ? null : evaluateHand(cards);

  return (
    <div className={`hand ${active ? "hand-active" : ""}`}>
      {label && <div className="hand-label">{label}</div>}
      <div className="hand-cards">
        {visibleCards.map((card, i) => (
          <Card key={card.id ?? i} card={card} />
        ))}
        {hideSecondCard && <Card faceDown />}
      </div>
      <div className="hand-meta">
        {evalResult && (
          <span className="hand-total">
            {evalResult.isBust ? "Bust" : evalResult.isBlackjack ? "Blackjack!" : evalResult.soft ? `Soft ${evalResult.total}` : evalResult.total}
          </span>
        )}
        {typeof bet === "number" && bet > 0 && <span className="hand-bet">Bet: {bet}</span>}
      </div>
    </div>
  );
}
