-- 5-valid_email.sql

-- Drop trigger if it already exists
DROP TRIGGER IF EXISTS reset_valid_email_on_change;

-- Create the trigger that resets the valid_email attribute when the email changes
CREATE TRIGGER reset_valid_email_on_change
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
