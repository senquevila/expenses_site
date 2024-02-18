# Changelog
## 2024-02-18
### New
- `account_type` in account model.
- Changelog template: Add New, Fixed and Removed subtitles.
### Fixed
- Cascade delete on foreign key fields.
- Upload Result template.
- Budget assignaments.
### Removed
- swap account view.
- Category and MatchAccount models.

## 2024-02-04
### New
- Periods activation.
- Admin forms actions: remove blank uploads, remove invalid expenses, disabled periods.
### Fixed
- Upload expense result giving detail for all the rows.

## 2024-01-28
### New
- Redux URLs.
- Update expenses in the budget.
- List expense categories associated in the budget.
- Result from expense upload.
### Fixed
- Cleanup the DB when a upload does not have expenses associated.

## 2024-01-21
- Expenses CRUD forms.
- Upload model.
- Show results from upload an expense file.

## 2024-01-14
### New
- Budget app.
- Translate account.

## 2024-01-13
### New
- Automation for associating accounts by searching for reserved tokens in expense descriptions.

## 2024-01-04
### New
- Open periods endpoint.
- Link to use CDN font from bootstrap.
### Fixed
- Changelog format. Using the verbs: Added, Changed and Removed

## 2024-01-01
### New
- Bank and BankAccount models.
### Removed
- Removed not used API endpoints.

## 2023-12-31
### Fixed
- Changed Filter to omit closed period in the expenses uploads.
### Removed
- Period from upload expenses. This field will be calculated from the payment date.

## 2023-11-04
### New
- `local_amount` field on Expense model.
- `populate_local_amount` command.
- `refresh_period_total` command.
- USD convertion when upload expenses.

## 2023-10-15
### New
- Convertion object when it is created.
- Script to call the convertion endpoint.

## 2023-10-03
### New
- Account list.
- Currency convert list.
- home.html

## 2023-09-24
### New
- Close a period.
- HTML templates for list periods and expenses.
- HTML templates for uploading expenses CSV files.