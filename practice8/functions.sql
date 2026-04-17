DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE OR REPLACE FUNCTION search_contacts(search_text VARCHAR)
RETURNS TABLE(out_username VARCHAR, out_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.username AS out_username,
           pb.phone AS out_phone
    FROM phonebook AS pb
    WHERE pb.username ILIKE '%' || search_text || '%'
       OR pb.phone ILIKE '%' || search_text || '%';
END;
$$ LANGUAGE plpgsql;

-- Test:
-- SELECT * FROM search_contacts('test');

-- ============================================
-- 2. Function: get_contacts_paginated
-- Returns a limited number of contacts with offset
-- ============================================

-- Drop old function if exists
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);

-- Create the function
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(out_username VARCHAR, out_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.username AS out_username,
           pb.phone AS out_phone
    FROM phonebook AS pb
    ORDER BY pb.username   -- optional: ensure consistent ordering
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;

-- Test:
-- SELECT * FROM get_contacts_paginated(5, 0);