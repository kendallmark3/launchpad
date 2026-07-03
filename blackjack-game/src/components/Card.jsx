const RED_SUITS = new Set(["♥", "♦"]);

export function Card({ card, faceDown = false }) {
  if (faceDown) {
    return (
      <div className="card card-face-down" aria-label="Hidden card">
        <div className="card-back-pattern" />
      </div>
    );
  }

  const isRed = RED_SUITS.has(card.suit);
  return (
    <div className={`card ${isRed ? "card-red" : "card-black"}`} aria-label={`${card.rank} of ${card.suit}`}>
      <span className="card-rank card-rank-top">{card.rank}</span>
      <span className="card-suit">{card.suit}</span>
      <span className="card-rank card-rank-bottom">{card.rank}</span>
    </div>
  );
}
