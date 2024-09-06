CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role INTEGER NOT NULL
);

CREATE TABLE wallet (
    user_id INTEGER,
    stock TEXT NOT NULL,
    qtd INTEGER NOT NULL,
    avg_price REAL NOT NULL,
    avg_cost REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

