*********
Changelog
*********


development
===========
- Improve installation documentation
- Mitigate ``400 Bad Request`` responses when receiving GET requests with
  empty HTTP request bodies but still setting ``Content-Type: application/json``.
  Thanks for the report, @byteptr and @MichielKE!
- Improve installation instructions for Windows. Thanks, @MichielKE!
- Improve documentation
- Initialize Flask logger appropriately
- Add capability for request/response logging
- Format the code with black and isort


2022-01-22 0.2.0
================
- Add example for annotating phenology data within Grafana
- Change license to AGPL-3.0
- Modernize dependency versions. Drop support for Python 3.6.
- Improve sandbox environment setup and documentation


2020-12-27 0.1.2
================
- Adjust documentation


2020-12-27 0.1.1
================
- Adjust documentation


2020-12-27 0.1.0
================
- First official release
