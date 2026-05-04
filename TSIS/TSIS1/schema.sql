-- Drop tables if they already exist (to avoid conflicts during re-run)
DROP TABLE IF EXISTS phones CASCADE;
DROP TABLE IF EXISTS contacts CASCADE;
DROP TABLE IF EXISTS groups CASCADE;

-- Table for grouping contacts (categories)
-- Example: Family, Work, Friend
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,             -- unique group ID
    name VARCHAR(50) UNIQUE NOT NULL   -- group name must be unique
);

-- Main contacts table
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,                 -- unique contact ID
    username VARCHAR(50) UNIQUE NOT NULL,  -- contact name (unique)
    email VARCHAR(100),                    -- email field
    birthday DATE,                         -- birthday (DATE type)
    group_id INTEGER REFERENCES groups(id), -- foreign key to groups
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- auto timestamp
);

-- Phones table (1 contact → many phones)
CREATE TABLE phones (
    id SERIAL PRIMARY KEY,                     -- unique phone ID
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    -- if contact is deleted → all phones are deleted automatically

    phone VARCHAR(20) NOT NULL,               -- phone number

    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
    -- restrict phone type to valid values only
);

-- Insert default groups (ignore if already exists)
INSERT INTO groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;