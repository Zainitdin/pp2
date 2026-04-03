--Pattern Search Function
CREATE OR REPLACE FUNCTION search_contacts(p_text text)
RETURNS TABLE(out_username VARCHAR, out_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.username AS out_username, pb.phone AS out_phone
    FROM phonebook pb
    WHERE pb.username ILIKE '%' || p_text || '%'
       OR pb.phone ILIKE '%' || p_text || '%';
END;


-- Specify procedural language
$$ LANGUAGE plpgsql;

--Pagination function

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT username, phone
    FROM phonebook
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;