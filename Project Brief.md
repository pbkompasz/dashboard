# Project Brief

 We are building a platform a user to login and create & submit orders for our print on demand software.

## Homepage
- Main Feature => User Login

- User Logged In (/dashboard)

- Orders — /dashboard/orders
- Catalog — /dasbhoard/catalog
- Upload CSV — /dashboard/upload
- Payments — /dashboard/payments

## Views under Orders
- OrderListView
  - List all Orders with Status, Date Placed, and Order Cost

- Order DetailView
  - Show the Details of Order, what is included, where it is shipping to and the status list.

- Order UpdateView
  - Ability to Cancel (if not in Production)
  - **Ability to Change Address (if not Shipped)

## Views under Catalog
- ProductListView
  - Show all Products available to user (some global, and some private)

- ProductCreateView
  - Allow User to Create a Private Product

- ProductUpdateView
  - If Product is Private, allow User to update the Product File

## Views under UploadCSV
- Simple View that a User Uploads a CSV file that processes the data and creates Orders

  - List Previously Uploaded CSVs & Status (Uploaded, Approved, Paid)

- Each batch of CSVs will automatically create a single Payment/Invoice.

- I think it would be nice to have a copy so we can always reference the original "just in case"

## Views under Payment
- List all Invoices Paid
  - Manage Payment Methods added (Credit Card or PayPal)

## Other Features Required.
- Basic API for Direct Order Upload
- direct order API:
  - POST /api/orders
    user sends a JSON that is similar to the structure of the CSV.
    it finds the first open invoice, or creates an open invoice, and adds to that invoic
