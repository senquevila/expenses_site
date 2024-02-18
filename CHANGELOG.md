# Changelog
## 2024-02-18
- Added account_type in account model.
- Removed swap account view.
- Changed cascade delete on foreign key fields.
- Fixed result template.

## 2024-02-04
- Added periods activation.
- Added admin forms actions: remove blank uploads, remove invalid expenses, disabled periods.
- Changed upload expense result giving detail for all the rows.

## 2024-01-28
- Redux URLs.
- Update expenses in the budget.
- List expense categories associated in the budget.
- Cleanup the DB when a upload does not have expenses associated.
- Add result from expense upload.

## 2024-01-21
- Expenses CRUD forms.
- Upload model.
- Show results from upload an expense file.

## 2024-01-14
- Added budget app.
- Added Translate account.

## 2024-01-13
- Added automation for associating accounts by searching for reserved tokens in expense descriptions.

## 2024-01-04
- Added open periods endpoint.
- Added link to use CDN font from bootstrap.
- Changed the Changelog format. Using the verbs: Added, Changed and Removed

## 2024-01-01
- Added Bank and BankAccount models.
- Removed not used API endpoints.

## 2023-12-31
- Changed Filter to omit closed period in the expenses uploads.
- Removed period from upload expenses. This field will be calculated from the payment date.

## 2023-11-04
- Added `local_amount` field on Expense model.
- Added `populate_local_amount` command.
- Added `refresh_period_total` command.
- Added usd convertion when upload expenses.

## 2023-10-15
- Added convertion object when it is created.
- Added script to call the convertion endpoint.

## 2023-10-03
- Added Account list.
- Added Currency convert list.
- Added home.html

## 2023-09-24
- Added period closing.
- Added HTML templates for list periods and expenses.
- Added HTML templates for uploading expenses CSV files.