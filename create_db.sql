CREATE TABLE categories (
    codename VARCHAR(255) PRIMARY KEY,  -- Название категории
    name VARCHAR(255)
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,              -- Уникальный идентификатор продукта
    name VARCHAR(255) NOT NULL,          -- Название продукта
    price DECIMAL(10, 2) NOT NULL,       -- Цена продукта
    category_name VARCHAR(255),          -- Ссылка на категорию (тип данных должен быть VARCHAR(255))

    -- Установка внешнего ключа для связи с таблицей categories
    FOREIGN KEY (category_name) 
        REFERENCES categories(codename)
        ON DELETE CASCADE                -- Удаление всех продуктов при удалении категории
);


CREATE TABLE income (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);

-- Вставка данных в таблицу categories
INSERT INTO categories (codename, name) VALUES 
('eat', 'Еда'),
('transport', 'Транспорт'),
('ethernat pay', 'Интернет покупки'),
('other', 'Другое');
