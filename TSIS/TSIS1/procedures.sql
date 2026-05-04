-- Procedure: add a new phone to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER; -- variable to store contact ID
BEGIN
    -- Find contact ID by username
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    -- If contact does not exist → stop execution
    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    -- Insert new phone into phones table
    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- Procedure: move contact to another group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    -- Create group if it does not exist
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    -- Update contact's group
    UPDATE contacts
    SET group_id = v_group_id
    WHERE username = p_contact_name;
END;
$$;


-- Function: search across all fields
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.username,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id

    -- Search across multiple fields (name, email, phone, group)
    WHERE 
        c.username ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
        OR g.name ILIKE '%' || p_query || '%';
END;
$$;


-- Function: pagination using LIMIT and OFFSET
DROP FUNCTION IF EXISTS get_contacts_paginated(integer, integer)
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offst INT)
RETURNS TABLE (
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.username,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    ORDER BY c.id
    LIMIT lim OFFSET offst;
END;
$$;