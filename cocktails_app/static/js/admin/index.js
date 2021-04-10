/**
 * Note: changes to this file don't show up until the python server is
 * restarted (because python reads the manifest on boot).
 */
import $ from 'jquery';

// import chosen while disabling linting; by importing it at all it allows
// $(el).chosen() to work.
import chosen from 'chosen-js'; // eslint-disable-line

import 'chosen-js/chosen.css';
import './index.scss';

const SELECTS = '.form-row:not(.empty-form) .field-ingredient select';
const REFRESH_INTERVAL = 1000;
let ingredientCounts = [];

const bindChosen = () => {
  $(SELECTS).chosen();
};

const getIngredientCounts = () => (
  $(SELECTS).map((i, el) => $(el).find('option').length)
);

// loop through the selects and compare the number of ingredients to the
// previous run's number of ingredients. if they differ, update chosen.
const updateChosens = () => {
  const newIngredientCounts = getIngredientCounts();

  ingredientCounts.each((i, count) => {
    if (count === newIngredientCounts[i]) {
      return;
    }

    $(SELECTS).eq(i).trigger('chosen:updated');
  });

  ingredientCounts = newIngredientCounts;
};

$(() => {
  // short circuit on admin pages without selects
  if (!$(SELECTS).length) {
    return;
  }

  // bind initial dropdown
  bindChosen();

  // when we add an ingredient row, bind dropdowns again
  $('.add-row a').on('click', bindChosen);

  // get the initial ingredient counts
  ingredientCounts = getIngredientCounts();

  // refresh the list of chosen options on an interval to catch newly added
  // options
  setInterval(() => updateChosens(), REFRESH_INTERVAL);
});
