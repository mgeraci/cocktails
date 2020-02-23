/* global document */
import Fastclick from 'fastclick';

import Login from './login';
import MobileMenu from './mobileMenu';
import Recipe from './recipe';
import Search from './search';

import '../css/styles.sass';

Fastclick.attach(document.body);

Login.init();
MobileMenu.init();
Recipe.init();
Search.init();
