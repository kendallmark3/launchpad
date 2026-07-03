import { describe, expect, it } from "vitest";
import { dealerShouldHit, playDealerHand } from "./dealer.js";

const card = (rank, suit = "♠") => ({ rank, suit, id: `${rank}${suit}` });

describe("dealerShouldHit", () => {
  it("hits below 17", () => {
    expect(dealerShouldHit([card("9"), card("6")])).toBe(true);
  });

  it("stands on a hard 17", () => {
    expect(dealerShouldHit([card("10"), card("7")])).toBe(false);
  });

  it("stands on a soft 17", () => {
    expect(dealerShouldHit([card("A"), card("6")])).toBe(false);
  });

  it("stands on any total above 17", () => {
    expect(dealerShouldHit([card("K"), card("Q")])).toBe(false);
  });
});

describe("playDealerHand", () => {
  it("draws cards until reaching at least 17", () => {
    const drawSequence = [card("10"), card("5")];
    const drawCard = () => drawSequence.shift();

    const finalHand = playDealerHand([card("2"), card("2")], drawCard);

    expect(finalHand).toHaveLength(4);
    expect(finalHand.map((c) => c.rank)).toEqual(["2", "2", "10", "5"]);
  });

  it("draws nothing when already at 17+", () => {
    const drawCard = () => {
      throw new Error("should not draw");
    };

    const finalHand = playDealerHand([card("K"), card("8")], drawCard);

    expect(finalHand).toHaveLength(2);
  });
});
