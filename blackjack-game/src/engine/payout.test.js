import { describe, expect, it } from "vitest";
import { OUTCOMES, resolveHand, resolveInsurance } from "./payout.js";

describe("resolveHand", () => {
  it("player bust always loses, even if the dealer would also have busted", () => {
    const result = resolveHand({ playerTotal: 25, playerBust: true, dealerTotal: 24, dealerBust: true, bet: 10 });
    expect(result).toEqual({ outcome: OUTCOMES.LOSS, payout: -10 });
  });

  it("player natural blackjack pays 3:2", () => {
    const result = resolveHand({ playerTotal: 21, playerIsNatural: true, dealerTotal: 18, bet: 10 });
    expect(result).toEqual({ outcome: OUTCOMES.BLACKJACK, payout: 15 });
  });

  it("both natural blackjacks push", () => {
    const result = resolveHand({ playerTotal: 21, playerIsNatural: true, dealerTotal: 21, dealerIsNatural: true, bet: 10 });
    expect(result).toEqual({ outcome: OUTCOMES.PUSH, payout: 0 });
  });

  it("dealer natural beats a non-natural 21 (e.g. after a split)", () => {
    const result = resolveHand({ playerTotal: 21, playerIsNatural: false, dealerTotal: 21, dealerIsNatural: true, bet: 10 });
    expect(result).toEqual({ outcome: OUTCOMES.LOSS, payout: -10 });
  });

  it("dealer bust pays even money", () => {
    const result = resolveHand({ playerTotal: 18, dealerTotal: 24, dealerBust: true, bet: 10 });
    expect(result).toEqual({ outcome: OUTCOMES.WIN, payout: 10 });
  });

  it("higher total wins", () => {
    expect(resolveHand({ playerTotal: 19, dealerTotal: 18, bet: 10 })).toEqual({ outcome: OUTCOMES.WIN, payout: 10 });
    expect(resolveHand({ playerTotal: 17, dealerTotal: 18, bet: 10 })).toEqual({ outcome: OUTCOMES.LOSS, payout: -10 });
  });

  it("equal totals push", () => {
    expect(resolveHand({ playerTotal: 18, dealerTotal: 18, bet: 10 })).toEqual({ outcome: OUTCOMES.PUSH, payout: 0 });
  });
});

describe("resolveInsurance", () => {
  it("pays 2:1 when the dealer has blackjack", () => {
    expect(resolveInsurance({ insuranceBet: 5, dealerIsNatural: true })).toBe(10);
  });

  it("loses the insurance bet when the dealer doesn't have blackjack", () => {
    expect(resolveInsurance({ insuranceBet: 5, dealerIsNatural: false })).toBe(-5);
  });

  it("is a no-op when no insurance was taken", () => {
    expect(resolveInsurance({ insuranceBet: 0, dealerIsNatural: true })).toBe(0);
  });
});
