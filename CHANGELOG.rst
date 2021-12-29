Changelog
=========
1.7.0
-------------------
- Added missing webhook groups
- Added webhooks for Transfers
- Added taxVerificationStatus to User
- Added Document and RejectReason models
- Updated filters for list endpoints

1.6.0
-------------------
- Added custom headers
- Added filters
- Added status transitions for Transfers, TransferRefunds

1.5.1
-------------------
- Added field 'processingTime' to BankCards
- Added field 'expiresOn' to Payments

1.5.0
-------------------
- Added Venmo accounts
- Added User status transitions
- Added Transfer refunds
- Added upload multipart documents feature

1.4.0
-------------------
- Fix TypeError thrown when response status is 204 No content
- Fix tests for python 3
- Add updatePayPalAccount()
- Python uses os path join url causing issues on windows
- Add CVV field to the sdk
- Remove Relationship field from Server SDK
- Add Business Operating Name Field to User
- Add PayPal account status transitions

1.3.0 (2019-01-28)
-------------------
- Added field "VerificationStatus" to User
- Client-token endpoint renamed to authentication-token

1.2.1 (2019-01-17)
------------------

- FIX: Resolved issue with restricted "Accept" & "Content-Type" headers to support only "application/json" or "application/jose+json"

1.2.0 (2018-12-20)
------------------

- Restricted “Accept” & “Content-Type” headers to support only “application/json” or “application/jose+json”
- Related resources “relatedResources” in error representation is added
- Added Authentication token endpoint

1.1.4 (2018-12-04)
------------------

- Added PayPal account endpoint

1.1.3 (2018-07-05)
------------------

- Added transfer endpoint

1.1.2 (2018-03-20)
------------------

- Added bank card endpoint

1.1.1 (2017-10-11)
------------------

- Bumped version and first public release!

1.1.0 (2017-09-29)
------------------

- Completed coverage of all endpoints
- 100% code coverage
- Audited available attributes for each model

1.0.0 (2017-08-04)
------------------

- Added support for resource types as models

0.2.0 (2016-12-22)
------------------

- Added support for all API endpoints
- Created package structure for distribution on PyPi
- Added tests

0.1.0 (2016-09-06)
------------------

- Repository creation
- Added license
- Added readme
