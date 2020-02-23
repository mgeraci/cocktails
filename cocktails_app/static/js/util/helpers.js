/* global window, document */

export const getScroll = () => {
  if (!window || !document) {
    return 0;
  }

  return window.pageYOffset
    || document.documentElement.scrollTop
    || document.body.scrollTop
    || 0;
};

export default {};
