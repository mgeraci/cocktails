/* global document */
import { Fraction } from 'fractional';

import { FRACTION_LOOKUP } from './util/constants';

const HIGHLIGHT_CLASS = 'highlight';
const MAX_QUANITITY = 30;
const DIRECTIONS = {
  increment: 'increment',
  decrement: 'decrement',
};

const Recipe = {
  init() {
    if (!document.querySelectorAll('.page-recipe').length) {
      return;
    }

    this.steps = document.querySelectorAll('.step');

    this.listen();
    this.updateRecipeQuantities(1, {
      initialLoad: true,
    });

    document.querySelectorAll('.page-recipe-steps')[0].classList.remove('uninitialized');
  },

  listen() {
    const quantityButtons = document.querySelectorAll('.quantity-button');
    const stepAmounts = document.querySelectorAll('.step-amount');

    Array.from(quantityButtons).forEach((quantityButton) => {
      quantityButton.addEventListener('click', (e) => {
        const button = e.currentTarget;
        const field = button.closest('.quantity').querySelectorAll('input')[0];
        const direction = button.classList.contains('quantity-button--increment')
          ? 'increment'
          : 'decrement';

        this.changeValue(field, direction);
      });
    });

    Array.from(stepAmounts).forEach((amount) => {
      amount.addEventListener('animationend', (e) => {
        e.currentTarget.classList.remove(HIGHLIGHT_CLASS);
      });
    });
  },

  changeValue(field, direction) {
    let value = parseInt(field.getAttribute('value'), 10);

    if (direction === DIRECTIONS.increment) {
      value += 1;
    } else if (direction === DIRECTIONS.decrement) {
      value -= 1;
    }

    if (value < 1) {
      value = 1;
    } else if (value > MAX_QUANITITY) {
      value = MAX_QUANITITY;
    }

    field.setAttribute('value', value);
    this.updateRecipeQuantities(value);
  },

  updateRecipeQuantities(quantity, params = {}) {
    Array.from(this.steps).forEach((step) => {
      let amount = step.querySelectorAll('.step-amount');
      let unit = step.querySelectorAll('.step-unit');

      if (!amount.length) {
        return;
      }

      [amount] = amount;
      [unit] = unit;

      const num = amount.getAttribute('data-original-amount-num');
      const den = amount.getAttribute('data-original-amount-den');
      const newAmountFraction = new Fraction(num, den).multiply(quantity);

      amount.innerHTML = this.formatAmount(newAmountFraction);

      if (!params.initialLoad) {
        // trigger a reflow if the animation is currently happening (as
        // indicated by the animation class being present)
        if (amount.classList.contains(HIGHLIGHT_CLASS)) {
          amount.classList.remove(HIGHLIGHT_CLASS);
        }

        amount.classList.add(HIGHLIGHT_CLASS);
      }

      if (newAmountFraction > 1) {
        unit.innerHTML = unit.getAttribute('data-unit-plural');
      } else {
        unit.innerHTML = unit.getAttribute('data-unit-singular');
      }
    });
  },

  // split the fraction into the integer and a fraction
  formatAmount(fraction) {
    const numerator = fraction.numerator % fraction.denominator;
    const int = Math.floor(fraction.numerator / fraction.denominator);
    const fractionCharacter = FRACTION_LOOKUP[numerator] != null
      ? FRACTION_LOOKUP[numerator][fraction.denominator]
      : undefined;

    if (fractionCharacter) {
      if (int) {
        return `${int} ${fractionCharacter}`;
      }

      return fractionCharacter;
    }

    return fraction.toString();
  },
};

export default Recipe;
