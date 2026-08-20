-- FlyRank BE-08 PDF Report Generator Database Schema

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    price_gbp DECIMAL(10, 2),
    availability VARCHAR(200),
    rating VARCHAR(50),
    description TEXT,
    product_url VARCHAR(500),
    source_page VARCHAR(500),
    fetched_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_books_category ON books(category);
CREATE INDEX IF NOT EXISTS idx_books_price ON books(price_gbp);
CREATE INDEX IF NOT EXISTS idx_books_fetched_at ON books(fetched_at);

-- Sample data for testing (matches BE-05 scraper output)
INSERT INTO books (title, category, price_gbp, availability, rating, description, product_url, source_page, fetched_at) VALUES
('A Light in the Attic', 'fiction', 51.77, 'In stock', 'Three', 'Poetry from Shel Silverstein.', 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Tipping the Velvet', 'fiction', 53.74, 'In stock', 'One', 'A historical novel.', 'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Soumission', 'fiction', 50.10, 'In stock', 'One', 'A novel by Michel Houellebecq.', 'https://books.toscrape.com/catalogue/soumission_998/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Sharp Objects', 'fiction', 47.82, 'In stock', 'Four', 'A psychological thriller.', 'https://books.toscrape.com/catalogue/sharp-objects_997/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Sapiens: A Brief History of Humankind', 'nonfiction', 54.23, 'In stock', 'Five', 'A book by Yuval Noah Harari.', 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html', '/catalogue/category/books_1/index.html', NOW()),
('The Power of Habit', 'self_help', 38.99, 'In stock', 'Four', 'Why we do what we do in life and business.', 'https://books.toscrape.com/catalogue/the-power-of-habit_995/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Atomic Habits', 'self_help', 42.50, 'In stock', 'Five', 'An easy & proven way to build good habits.', 'https://books.toscrape.com/catalogue/atomic-habits_994/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Harry Potter and the Philosopher''s Stone', 'children', 29.99, 'In stock', 'Five', 'The first Harry Potter book.', 'https://books.toscrape.com/catalogue/harry-potter-and-the-philosophers-stone_993/index.html', '/catalogue/category/books_1/index.html', NOW()),
('The Very Hungry Caterpillar', 'children', 15.99, 'In stock', 'Five', 'Classic children''s book.', 'https://books.toscrape.com/catalogue/the-very-hungry-caterpillar_992/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Clean Code', 'nonfiction', 44.95, 'In stock', 'Five', 'A handbook of agile software craftsmanship.', 'https://books.toscrape.com/catalogue/clean-code_991/index.html', '/catalogue/category/books_1/index.html', NOW()),
('Design Patterns', 'nonfiction', 52.00, 'In stock', 'Four', 'Elements of reusable object-oriented software.', 'https://books.toscrape.com/catalogue/design-patterns_990/index.html', '/catalogue/category/books_1/index.html', NOW()),
('The Pragmatic Programmer', 'nonfiction', 48.50, 'In stock', 'Five', 'Your journey to mastery.', 'https://books.toscrape.com/catalogue/the-pragmatic-programmer_989/index.html', '/catalogue/category/books_1/index.html', NOW());