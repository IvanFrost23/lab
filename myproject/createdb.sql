CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    publication_year INT
);

INSERT INTO books (title, author, price, publication_year)
VALUES
    ('War and Peace', 'Leo Tolstoy', 29.99, 1869),
    ('1984', 'George Orwell', 8.99, 1949),
    ('Crime and Punishment', 'Fyodor Dostoevsky', 14.99, 1867),
    ('Pride and Prejudice', 'Jane Austen', 9.99, 1813),
    ('Moby Dick', 'Herman Melville', 11.50, 1851);