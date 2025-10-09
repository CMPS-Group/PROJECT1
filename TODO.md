# Inventory Management System Implementation

## Completed Features
- [x] Added InventoryLog model to track inventory changes
- [x] Added created_at field to Order model
- [x] Seller endpoints:
  - [x] PUT /seller/vehicles/<id>/inventory - Update inventory separately
  - [x] GET /seller/inventory/alerts - Get low stock alerts
  - [x] GET /seller/inventory/restock-suggestions - Automatic restock suggestions
- [x] Admin endpoints:
  - [x] GET /admin/inventory - View all vehicle inventories
  - [x] GET /admin/inventory/logs - View inventory logs
- [x] Updated checkout process to log inventory changes
- [x] App starts without errors

## Testing Tasks
- [ ] Test seller inventory update endpoint
- [ ] Test low stock alerts endpoint
- [ ] Test restock suggestions endpoint
- [ ] Test admin inventory view endpoint
- [ ] Test admin inventory logs endpoint
- [ ] Test checkout with inventory logging
- [ ] Verify database tables are created correctly

## Notes
- Inventory changes are logged with user_id as the seller's id for checkout reductions
- Restock suggestions use a simple heuristic based on recent sales
- Low stock threshold defaults to 10 but can be customized via query param
