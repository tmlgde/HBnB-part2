-- Admin user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$3jHBoGllsOJ6RZwGbznJK.SZpEPZidwuXKH2n2CVMBkZsLw5iFwF6',
    TRUE
);

-- Initial amenities
INSERT INTO amenities (id, name)
VALUES
    ('6f6e1bb2-2e9c-4fc7-b131-2f70b88b2c91', 'WiFi'),
    ('f410e2a1-883f-4f8d-8b52-5f67b426ab2f', 'Swimming Pool'),
    ('adc390e4-938f-4b0f-b3e5-d1db6bbf25d4', 'Air Conditioning');
