import { describe, expect, it } from "vitest";
import { evaluateHand, isPair } from "./hand.js";

const card = (rank, suit = "♠") => ({ rank, suit, id: `${rank}${suit}` });

describe("evaluateHand", () => {
  it("sums simple hard hands", () => {
    const result = evaluateHand([card("9"), card("7")]);
    expect(result).toMatchObject({ total: 16, soft: false, isBust: false, isBlackjack: false });
  });

  it("counts a single ace as 11 when it fits", () => {
    const result = evaluateHand([card("A"), card("6")]);
    expect(result).toMatchObject({ total: 17, soft: true });
  });

  it("detects a natural blackjack", () => {
    const result = evaluateHand([card("A"), card("K")]);
    expect(result).toMatchObject({ total: 21, isBlackjack: true });
  });

  it("demotes an ace to 1 to avoid busting", () => {
    const result = evaluateHand([card("A"), card("9"), card("5")]);
    expect(result).toMatchObject({ total: 15, soft: false });
  });

  it("handles multiple aces correctly", () => {
    const result = evaluateHand([card("A"), card("A"), card("9")]);
    expect(result).toMatchObject({ total: 21, soft: true });
  });

  it("handles three aces without busting", () => {
    const result = evaluateHand([card("A"), card("A"), card("A")]);
    expect(result).toMatchObject({ total: 13, soft: true });
  });

  it("detects a bust", () => {
    const result = evaluateHand([card("K"), card("Q"), card("5")]);
    expect(result).toMatchObject({ total: 25, isBust: true });
  });

  it("a 21 after more than two cards is not a natural blackjack", () => {
    const result = evaluateHand([card("7"), card("7"), card("7")]);
    expect(result).toMatchObject({ total: 21, isBlackjack: false });
  });
});

describe("isPair", () => {
  it("is true for two cards of the same value", () => {
    expect(isPair([card("K"), card("Q")])).toBe(true);
    expect(isPair([card("8"), card("8")])).toBe(true);
  });

  it("is false for two cards of different values", () => {
    expect(isPair([card("8"), card("9")])).toBe(false);
  });

  it("is false once a hand has more than two cards", () => {
    expect(isPair([card("8"), card("8"), card("2")])).toBe(false);
  });
});
