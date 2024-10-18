-- 4-store.sql

-- Drop trigger if it already exists
DROP TRIGGER IF EXISTS decrease_quantity_on_new_order;

-- Create a trigger that updates the quantity in 'items' table after an insert in 'orders'
CREATE TRIGGER decrease_quantity_on_new_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
