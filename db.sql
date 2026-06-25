---already defined the product table from terminal
---create new vendor table
create table vendor(
    vendor_id int generated always as identity primary key,
    vendor_name varchar(200) not null unique,
    base_url varchar(200) not null unique
);

---create the price table
create table price_hostory(
    price_id int generated always as identity primary key,
    product_id int not null references products(product_id),
    vendor_id int not null references vendor(vendor_id),
    price decimal(10,2) not null,
    created_at timestamp default current_timestamp
);