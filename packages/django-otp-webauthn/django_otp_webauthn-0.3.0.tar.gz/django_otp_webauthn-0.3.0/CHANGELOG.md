# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-08-03

## Changed

- The built-in Passkey registration and verification views error handling has been reworked. ([#12](https://github.com/Stormbase/django-otp-webauthn/pull/12) by [Stormheg](https://github.com/Stormheg))

## Fixed

- A regression in v0.2.0 was fixed were `AuthenticationDisabled` would incorrectly be raised. (Issue [#10](https://github.com/Stormbase/django-otp-webauthn/issues/10) by [jmichalicek](https://github.com/jmichalicek); fixed in [#12](https://github.com/Stormbase/django-otp-webauthn/pull/12) by [Stormheg](https://github.com/Stormheg))
- Support for `CSRF_USE_SESSIONS = True` was added. (Issue [#14](https://github.com/Stormbase/django-otp-webauthn/issues/14) by [nijel](https://github.com/nijel); fixed in [#15](https://github.com/Stormbase/django-otp-webauthn/issues/15) by [nijel](https://github.com/nijel) and [Stormheg](https://github.com/Stormheg))
- An issue that prevented MySQL from being used as the database backend was fixed. (Issue [#17](https://github.com/Stormbase/django-otp-webauthn/issues/17) by [nijel](https://github.com/nijel); fixed in [#18](https://github.com/Stormbase/django-otp-webauthn/issues/18) by [Stormheg](https://github.com/Stormheg))

## Removed

- The unused `RegistrationDisabled`, `AuthenticationDisabled`, and `LoginRequired` exceptions are removed. ([#12](https://github.com/Stormbase/django-otp-webauthn/pull/12) by [Stormheg](https://github.com/Stormheg))

## [0.2.0] - 2024-07-18

### Changed

- Support for having multiple `AUTHENTICATION_BACKENDS` was added. ([#8](https://github.com/Stormbase/django-otp-webauthn/pull/8) by [jmichalicek](https://github.com/jmichalicek))
  - **Action required:** add `django_otp_webauthn.backends.WebAuthnBackend` to your `AUTHENTICATION_BACKENDS` setting if you want to use passwordless login.

## [0.1.3] - 2024-07-01

### Added

- The default manager for the `WebAuthnCredential` model now includes a `as_credential_descriptors` method to make it easier to format the credentials for use in custom implementations.

### Fixed

- A bug was fixed with Python 3.11 and older that caused an exception when authenticating with a WebAuthn credential. ([#6](https://github.com/Stormbase/django-otp-webauthn/pull/6) by [jmichalicek](https://github.com/jmichalicek))

### Changed

- The `http://localhost:8000` default value for `OTP_WEBAUTHN_ALLOWED_ORIGINS` was removed.
- Use more appropriate examples for the `OTP_WEBAUTHN_*` settings in the README.
- Update admonition in the README to reflect the current state of the project. We have moved from don't use in production to use at your own risk.

## [0.1.2] - 2024-06-12

### Fixed

- The helper classes' `get_credential_display_name` and `get_credential_name` methods are now correctly called. Previously, the users' full name was being used as the credential name, bypassing above methods.

### Changed

- Set discoverable credential policy to `required` at registration time when `OTP_WEBAUTHN_ALLOW_PASSWORDLESS_LOGIN` is set to `True`. This is to ensure a credential capable of passwordless login is created.

### New

- Make is easier to override the helper class using the new `OTP_WEBAUTHN_HELPER_CLASS` setting. Pass it a dotted path to your custom helper class and it will be used instead of the default one.

## [0.1.1] - 2024-05-26

### Fixed

- An issue with the button label not showing any text was fixed.

### Changed

- `WebAuthnCredential` now inherits from `django_otp.models.TimestampMixin` to add a `created_at` and `last_used_at` fields. Subsequently, this raises the minimum `django-otp` version to `1.4.0+`.

### Maintenance

- Switch to [`hatch`](https://hatch.pypa.io/) for managing the project.

## [0.1.0] - 2024-05-12

- Initial release.
