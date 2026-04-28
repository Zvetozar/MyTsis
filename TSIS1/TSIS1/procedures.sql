CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    cid INTEGER;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;

    IF cid IS NOT NULL THEN
        INSERT INTO phones(contact_id, phone, type)
        VALUES (cid, p_phone, p_type);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    gid INTEGER;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES(p_group_name) RETURNING id INTO gid;
    END IF;

    UPDATE contacts SET group_id = gid WHERE name = p_contact_name;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name VARCHAR, email VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

-- 🔥 ПАГИНАЦИЯ В БД (как требует TSIS)
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE(name VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email
    FROM contacts c
    ORDER BY c.created_at
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;