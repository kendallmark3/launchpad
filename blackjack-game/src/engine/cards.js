export const SUITS = ["♠", "♥", "♦", "♣"];
export const RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];

export function cardValue(rank) {
  if (rank === "A") return 11;
  if (rank === "J" || rank === "Q" || rank === "K") return 10;
  return Number(rank);
}

export function createShoe(numDecks = 6) {
  const shoe = [];
  for (let deck = 0; deck < numDecks; deck++) {
    for (const suit of SUITS) {
      for (const rank of RANKS) {
        shoe.push({ rank, suit, id: `${rank}${suit}-${deck}` });
      }
    }
  }
  return shuffle(shoe);
}

export function shuffle(cards, random = Math.random) {
  const shuffled = cards.slice();
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

export function needsReshuffle(shoe, numDecks = 6) {
  return shoe.length < numDecks * 52 * 0.25;
}
