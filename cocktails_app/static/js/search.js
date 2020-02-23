/* global document */

const Search = {
  init() {
    const input = document.querySelectorAll('.page-content input[name=query]');

    if (
      !document.querySelectorAll('.page-search').length
      || !input.length
    ) {
      return;
    }

    setTimeout(() => {
      input[0].focus();
    }, 500);
  },
};

export default Search;
