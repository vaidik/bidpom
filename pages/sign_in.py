#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class SignIn(Base):

    _this_is_not_me_locator = (By.CSS_SELECTOR, '.isDesktop.thisIsNotMe')
    _signed_in_email_locator = (By.CSS_SELECTOR, 'label[for=email_0]')
    _emails_locator = (By.CSS_SELECTOR, 'label[for^=email_]')
    _email_locator = (By.ID, 'authentication_email')
    _login_password_locator = (By.ID, 'authentication_password')
    _register_password_locator = (By.ID, 'password')
    _verify_password_locator = (By.ID, 'vpassword')
    _desktop_next_locator = (By.CSS_SELECTOR, 'button.isDesktop.isStart')
    _mobile_next_locator = (By.CSS_SELECTOR, 'button.isMobile.isStart')
    _sign_in_locator = (By.CSS_SELECTOR, 'button.isReturning')
    _sign_in_returning_user_locator = (By.ID, 'signInButton')
    _verify_email_locator = (By.ID, 'verify_user')
    _gmail_email_locator = (By.CSS_SELECTOR, '#gaia_loginform #Email')
    _gmail_password_locator = (By.CSS_SELECTOR, '#gaia_loginform #Passwd')
    _gmail_sign_in_button_locator = (By.CSS_SELECTOR, '#gaia_loginform #signIn')
    _forgot_password_locator = (By.CSS_SELECTOR, '.isDesktop.forgotPassword')
    _reset_password_locator = (By.ID, 'password_reset')
    _confirm_message_locator = (By.XPATH, "//h2[.='Confirm your email address']")
    _check_email_at_locator = (By.CSS_SELECTOR, '#wait .contents h2 + p strong')
    _add_another_email_locator = (By.CSS_SELECTOR, '.isDesktop.useNewEmail')
    _new_email_locator = (By.ID, 'newEmail')
    _add_new_email_locator = (By.ID, 'addNewEmail')
    _your_computer_content_locator = (By.ID, 'your_computer_content')
    _this_is_my_computer_locator = (By.ID, 'this_is_my_computer')
    _this_is_not_my_computer_locator = (By.ID, 'this_is_not_my_computer')

    def __init__(self, selenium, timeout, expect='new'):
        Base.__init__(self, selenium, timeout)

        if self.selenium.title != self._page_title:
            for handle in self.selenium.window_handles:
                self.selenium.switch_to_window(handle)
                WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
                if self.selenium.title == self._page_title:
                    break
            else:
                raise Exception('Popup has not loaded')

        if expect == 'new':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(*self._email_locator).is_displayed())
        elif expect == 'returning':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._sign_in_returning_user_locator).is_displayed())
            import time
            time.sleep(2)  # TODO: Remove this sleep
        else:
            raise Exception('Unknown expect value: %s' % expect)

    @property
    def signed_in_email(self):
        """Get the value of the email that is currently signed in."""
        return self.selenium.find_element(*self._signed_in_email_locator).get_attribute('value')

    def click_this_is_not_me(self):
        """Clicks the 'This is not me' button."""
        self.selenium.find_element(*self._this_is_not_me_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._email_locator).is_displayed())

    @property
    def emails(self):
        """Get the emails for the returning user."""
        return [element.text for element in
                self.selenium.find_elements(*self._emails_locator)]

    @property
    def email(self):
        """Get the value of the email field."""
        return self.selenium.find_element(*self._email_locator).get_attribute('value')

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        email = self.selenium.find_element(*self._email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def new_email(self):
        """Get the value of the new email field."""
        return self.selenium.find_element(*self._new_email_locator).get_attribute('value')

    @new_email.setter
    def new_email(self, value):
        """Set the value of the new email field."""
        email = self.selenium.find_element(*self._new_email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def selected_email(self):
        """Return the value of the selected email of returning user's multiple emails"""
        for email in self.selenium.find_elements(*self._emails_locator):
            if email.find_element(By.TAG_NAME, 'input').is_selected():
                return email.text

    def select_email(self, value):
        """Select email from the returning user's multiple emails."""
        for email in self.selenium.find_elements(*self._emails_locator):
            if email.text == value:
                email.click()
                break
        else:
            raise Exception('Email not found: %s' % value)

    @property
    def register_password(self):
        """Get the value of the register password field."""
        return self.selenium.find_element(*self._register_password_locator).get_attribute('value')

    @register_password.setter
    def register_password(self, value):
        """Set the value of the register password field."""
        password = self.selenium.find_element(*self._register_password_locator)
        password.clear()
        password.send_keys(value)

    @property
    def login_password(self):
        """Get the value of the login password field."""
        return self.selenium.find_element(*self._login_password_locator).get_attribute('value')

    @login_password.setter
    def login_password(self, value):
        """Set the value of the login password field."""
        password = self.selenium.find_element(*self._login_password_locator)
        password.clear()
        password.send_keys(value)

    @property
    def verify_password(self):
        """Get the value of the verify password field."""
        return self.selenium.find_element(*self._verify_password_locator).get_attribute('value')

    @verify_password.setter
    def verify_password(self, value):
        """Set the value of the verify password field."""
        password = self.selenium.find_element(*self._verify_password_locator)
        password.clear()
        password.send_keys(value)

    @property
    def gmail_email(self):
        """Get the value of the email field from Gmail's login form."""
        return self.selenium.find_element(*self._gmail_email_locator).get_attribute('value')

    @gmail_email.setter
    def gmail_email(self, value):
        """Set the value of the email field in Gmail's login form."""
        email = self.selenium.find_element(*self._gmail_email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def gmail_password(self):
        """Get the value of the password field from Gmail's login form."""
        return self.selenium.find_element(*self._gmail_password_locator).get_attribute('value')

    @gmail_password.setter
    def gmail_password(self, value):
        """Set the value of the password field in Gmail's login form."""
        email = self.selenium.find_element(*self._gmail_password_locator)
        email.clear()
        email.send_keys(value)

    @property
    def check_email_at_address(self):
        """Get the value of the email address for confirmation."""
        return self.selenium.find_element(*self._check_email_at_locator).text

    def click_next(self, expect='password'):
        """Clicks the 'next' button."""

        if self.selenium.find_element(*self._desktop_next_locator).is_displayed():
            self.selenium.find_element(*self._desktop_next_locator).click()
        else:
            self.selenium.find_element(*self._mobile_next_locator).click()

        if expect == 'password':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._login_password_locator).is_displayed())
        elif expect == 'verify':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._verify_email_locator).is_displayed())
        elif expect == 'gmail':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._gmail_email_locator).is_displayed())
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def click_sign_in(self):
        """Clicks the 'sign in' button."""
        self.selenium.find_element(*self._sign_in_locator).click()
        self.switch_to_main_window()

    def click_gmail_sign_in(self):
        """Clicks the 'sign in' button in Gmail's login form."""
        self.selenium.find_element(*self._gmail_sign_in_button_locator).click()
        self.switch_to_main_window()

    def click_sign_in_returning_user(self, expect='login'):
        """Clicks the 'sign in' button."""
        self.selenium.find_element(
            *self._sign_in_returning_user_locator).click()

        if expect == 'login':
            self.switch_to_main_window()
        elif expect == 'remember':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._your_computer_content_locator).is_displayed())
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def click_verify_email(self):
        """Clicks 'verify email' button."""
        self.selenium.find_element(*self._verify_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._check_email_at_locator).is_displayed())

    def click_forgot_password(self):
        """Clicks 'forgot password' link (visible after entering a valid email)"""
        self.selenium.find_element(*self._forgot_password_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._confirm_message_locator).is_displayed())

    def click_reset_password(self):
        """Clicks 'reset password' after forgot password and new passwords entered"""
        self.selenium.find_element(*self._reset_password_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._check_email_at_locator).is_displayed())

    def click_add_another_email_address(self):
        """Clicks 'add another email' button."""
        self.selenium.find_element(*self._add_another_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._add_new_email_locator).is_displayed())

    def click_add_new_email(self):
        """Clicks 'Add' button to insert new email address."""
        self.selenium.find_element(*self._add_new_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._check_email_at_locator).is_displayed())

    def click_i_trust_this_computer(self):
        """Clicks 'I trust this computer' and signs in """
        self.selenium.find_element(*self._this_is_my_computer_locator).click()
        self.switch_to_main_window()

    def click_this_is_not_my_computer(self):
        """Clicks 'I trust this computer' and signs in for a public computer"""
        self.selenium.find_element(*self._this_is_not_my_computer_locator).click()
        self.switch_to_main_window()

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        if 'gmail' in email:
            self.click_next(expect='gmail')
            self.gmail_email = email
            self.gmail_password = password
            self.click_gmail_sign_in()
        else:
            self.click_next(expect='password')
            self.login_password = password
            self.click_sign_in()

    def sign_in_new_user(self, email, password):
        """Requests verification email using the specified email address."""
        self.email = email
        self.click_next(expect='verify')
        self.register_password = password
        self.verify_password = password
        self.click_verify_email()
        self.close_window()
        self.switch_to_main_window()

    def sign_in_returning_user(self):
        """Signs in with the stored user."""
        self.click_sign_in_returning_user()
