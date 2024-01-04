# Changelog

## 2024-01-01
### New
- Add Bank and BankAccount models.
- Remove not used API endpoints.

## 2023-12-31
### New
- Filter to omit closed period in the expenses uploads.

### Change
- Removed period from upload expenses. This field will be calculated from the payment date.

## 2023-11-04
### New
- Create `local_amount` field on Expense model.
- Create `populate_local_amount` command.
- Create `refresh_period_total` command.

### Change
- Create usd convertion when upload expenses.

## 2023-10-15
### Change
- Return the convertion object when it is created.
- Make an script to call the convertion endpoint.

## 2023-10-03
### New
- [Site] Account list.
- [Site] Currency convert list.

## Remove
- [Site] home.html

## 2023-09-24
### New
- Close a period.
- HTML templates for list periods and expenses.
- HTML templates for uploading expenses CSV files.