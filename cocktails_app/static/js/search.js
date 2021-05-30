/* global document */

const Search = {
  init() {
    this.autofocus();
    this.addKeyboardShortcut();
  },

  // mobile only, since the search page only exists on mobile
  autofocus() {
    const input = document.querySelectorAll('.page-content input[name=query]');

    if (
      !document.querySelectorAll('.page-search').length
      || !input.length
    ) {
      return;
    }

    setTimeout(() => {
      input[0].focus();
    }, 250);
  },

  addKeyboardShortcut() {
    const input = document.querySelectorAll('.page-header input[name=query]');

    if (
      !document.querySelectorAll('.desktop').length
      || !input.length
    ) {
      return;
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === '/') {
        e.preventDefault();
        input[0].focus();
      }
    });
  },
};

export default Search;
