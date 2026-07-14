CREATE TABLE products (
    product_id   INTEGER GENERATED ALWAYS AS IDENTITY,
    product_name VARCHAR(200) NOT NULL,
    category     VARCHAR(200) NOT NULL,
    base_price   REAL,
    CONSTRAINT products_pkey PRIMARY KEY (product_id),
    CONSTRAINT products_product_name_key UNIQUE (product_name)
);

CREATE TABLE vendor (
    vendor_id   INTEGER GENERATED ALWAYS AS IDENTITY,
    vendor_name VARCHAR(200) NOT NULL,
    base_url    VARCHAR(200) NOT NULL,
    CONSTRAINT vendor_pkey PRIMARY KEY (vendor_id),
    CONSTRAINT vendor_base_url_key UNIQUE (base_url),
    CONSTRAINT vendor_vendor_name_key UNIQUE (vendor_name)
);

CREATE TABLE price_history (
    price_id    INTEGER GENERATED ALWAYS AS IDENTITY,
    product_id  INTEGER NOT NULL,
    vendor_id   INTEGER NOT NULL,
    price       REAL NOT NULL,
    created_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT price_history_pkey PRIMARY KEY (price_id),
    CONSTRAINT price_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT price_history_vendor_id_fkey FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id)
);