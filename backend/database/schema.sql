CREATE TABLE product (
    id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    text TEXT,
    sentiment TEXT,
    FOREIGN KEY(product_id) REFERENCES product(id)
);
