-- 6-bonus.sql

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS AddBonus;

-- Create the stored procedure AddBonus
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;
    
    -- Check if the project exists; if it doesn't, insert it
    SELECT id INTO project_id 
    FROM projects 
    WHERE name = project_name 
    LIMIT 1;
    
    -- If project_id is NULL, the project does not exist, so create it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add the correction for the user and project
    INSERT INTO corrections (user_id, project_id, score) 
    VALUES (user_id, project_id, score);
END;
