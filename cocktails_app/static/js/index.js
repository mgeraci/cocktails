/* global document */
import Fastclick from 'fastclick';

import Login from './login';
import MobileMenu from './mobileMenu';
import Recipe from './recipe';
import Search from './search';
import { isMobile } from './util/helpers';

import '../css/styles.sass';

Fastclick.attach(document.body);

// add a body class for some minor style changes by platform
if (isMobile()) {
  document.body.classList.add('mobile');
} else {
  document.body.classList.add('desktop');
}

Login.init();
MobileMenu.init();
Recipe.init();
Search.init();
