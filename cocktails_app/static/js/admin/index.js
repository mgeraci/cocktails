import $ from 'jquery';

// import chosen, disable linting. this allows $(el).chosen() to work.
import chosen from 'chosen-js'; // eslint-disable-line

import 'chosen-js/chosen.css';
import './index.scss';

$(() => {
  $('.form-row:not(.empty-form) .field-ingredient select').chosen();

  $('.add-row a').on('click', () => {
    $('.form-row:not(.empty-form) .field-ingredient select').chosen();
  });
});
