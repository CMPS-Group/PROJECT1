# Inventory Management System Implementation

## Completed Features
- [x] Added InventoryLog model to track inventory changes
- [x] Added created_at field to Order model
- [x] Seller endpoints:
  - [x] PUT /seller/products/<id>/inventory - Update inventory separately
  - [x] GET /seller/inventory/alerts - Get low stock alerts
  - [x] GET /seller/inventory/restock-suggestions - Automatic restock suggestions
- [x] Admin endpoints:
  - [x] GET /admin/inventory - View all product inventories
  - [x] GET /admin/inventory/logs - View inventory logs
- [x] Updated checkout process to log inventory changes
- [x] App starts without errors
- [x] Push changes to GitHub and create PR
- [x] Renamed Vehicle to Product for generality
- [x] Updated all routes and models accordingly
- [x] Create requirements.txt with necessary dependencies
- [x] Create models.py for database models (User, Product, Order, CartItem, Discount)
- [x] Create auth.py for authentication and RBAC logic
- [x] Create routes/buyer.py for buyer endpoints (browse, cart, checkout)
- [x] Create routes/seller.py for seller endpoints (product management)
- [x] Create routes/admin.py for admin endpoints (orders, discounts, users)
- [x] Create app.py to set up Flask app and register blueprints

## Testing Tasks
- [x] Test seller inventory update endpoint
- [x] Test low stock alerts endpoint
- [x] Test restock suggestions endpoint
- [x] Test admin inventory view endpoint
- [x] Test admin inventory logs endpoint
- [x] Test checkout with inventory logging
- [x] Verify database tables are created correctly
- [x] Set up virtual environment and install dependencies
- [x] Run the app and perform basic testing (app starts successfully)

## Notes
- Inventory changes are logged with user_id as the seller's id for checkout reductions
- Restock suggestions use a simple heuristic based on recent sales
- Low stock threshold defaults to 10 but can be customized via query param
