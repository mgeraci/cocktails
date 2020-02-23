/* global document */

const FILLED_CLASS = 'filled';
const PASSWORD_LENGTH = 4;

const Login = {
  init() {
    if (!document.querySelectorAll('.page-login').length) {
      return;
    }

    this.form = document.querySelectorAll('.login-form');
    this.input = document.querySelectorAll('.page-login-fieldset-input');
    this.loginButtons = document.querySelectorAll('.login-button');
    this.indicators = document.querySelectorAll('.login-buttons-indicators-indicator');

    this.listen();
  },

  listen() {
    Array.from(this.loginButtons).forEach((loginButton) => {
      loginButton.addEventListener('click', this.onClick.bind(this));
      loginButton.addEventListener('tap', this.onClick.bind(this));
    });

    document.addEventListener('keydown', (e) => {
      this.handleInput(e.key);
    });
  },

  onClick(e) {
    this.handleInput(e.currentTarget.getAttribute('value'));
  },

  handleInput(value) {
    const currentPassword = this.input[0].getAttribute('value') || '';
    const newPassword = `${currentPassword}${value}`;

    this.input[0].setAttribute('value', newPassword);
    this.setIndicatorsTo(newPassword.length);

    if (newPassword.length === PASSWORD_LENGTH) {
      this.form[0].submit();
    }
  },

  setIndicatorsTo(count) {
    Array.from(this.indicators).forEach((indicator, i) => {
      if (i < count) {
        indicator.classList.add(FILLED_CLASS);
        return;
      }

      indicator.classList.remove(FILLED_CLASS);
    });
  },
};

export default Login;
