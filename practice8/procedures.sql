--DELETE PROCEDURE

-- Procedure to delete contact by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)

LANGUAGE plpgsql AS $$

BEGIN
    -- Delete row where username OR phone matches input
    DELETE FROM phonebook
    WHERE username = p_value OR phone = p_value;

END;

$$;

--Bulk Insert with Validation 

-- Procedure to insert multiple contacts with validation
CREATE OR REPLACE PROCEDURE bulk_insert()

LANGUAGE plpgsql AS $$

-- Declare variable to store each row
DECLARE
    rec RECORD;

BEGIN
    -- Loop through all rows in temporary table
    FOR rec IN SELECT * FROM temp_contacts LOOP

        -- Validate phone (only digits allowed)
        IF rec.phone ~ '^[0-9]+$' THEN

            -- If valid → insert or update
            CALL upsert_contact(rec.username, rec.phone);

        ELSE
            -- If invalid → show warning
            RAISE NOTICE 'Invalid phone: %', rec.phone;

        END IF;

    END LOOP;

END;

$$;

--UPSERT PROCEDURE

-- Create procedure to insert or update contact
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)

-- Define language
LANGUAGE plpgsql AS $$

BEGIN
    -- Check if user already exists
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_name) THEN
        
        -- If exists → update phone
        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_name;

    ELSE
        -- If not exists → insert new contact
        INSERT INTO phonebook(username, phone)
        VALUES(p_name, p_phone);

    END IF;

END;

$$;