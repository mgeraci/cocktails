/* global window, document */
import debounce from 'just-debounce';

import { getScroll } from './util/helpers';

const DOWN_CLASS = 'mobile-menu--down';

const MobileMenu = {
  init() {
    [this.menu] = document.querySelectorAll('.mobile-menu');
    this.maxScroll = document.body.scrollHeight - window.innerHeight;
    this.lastScroll = getScroll();

    let atStart = true;
    this.scrollWatcher();
    this.dbScrollStart = debounce(this.onScroll, 100, atStart);
    atStart = false;
    this.dbScrollEnd = debounce(this.onScroll, 100, atStart);
  },

  scrollWatcher() {
    document.addEventListener('scroll', () => {
      this.dbScrollStart();
      this.dbScrollEnd();
    });

    document.addEventListener('touchmove', () => {
      this.onScroll();
    });
  },

  onScroll() {
    let scroll = getScroll();

    // keep scroll in bounds to counteract measuring the 'rubber band' effect
    // on iOS
    if (scroll > this.maxScroll) {
      scroll = this.maxScroll;
    }

    if (scroll === this.lastScroll) { return; }

    if ((scroll > this.lastScroll) && !this.menu.classList.contains(DOWN_CLASS)) {
      this.menu.classList.add(DOWN_CLASS);
    } else if ((scroll < this.lastScroll) && this.menu.classList.contains(DOWN_CLASS)) {
      this.menu.classList.remove(DOWN_CLASS);
    }

    this.lastScroll = scroll;
  },
};

export default MobileMenu;
