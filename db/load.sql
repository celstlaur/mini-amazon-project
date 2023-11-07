\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY OrderFact FROM 'OrderFact.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orderfact_id_seq',
                         (SELECT MAX(id)+1 FROM OrderFact),
                         false);

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Balance FROM 'Balance.csv' WITH DELIMITER ',' NULL '' CSV

\COPY CartContents FROM 'CartContents.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Fulfills FROM 'Fulfills.csv' WITH DELIMITER ',' NULL '' CSV

\COPY HasInventory FROM 'HasInventory.csv' WITH DELIMITER ',' NULL '' CSV

\COPY OrderContents FROM 'OrderContents.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ReviewedProduct FROM 'ReviewedProduct.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ReviewedSeller FROM 'ReviewedSeller.csv' WITH DELIMITER ',' NULL '' CSV

\COPY SavedForLaterContents FROM 'SavedForLaterContents.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Search FROM 'Search.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Wishes FROM 'Wishes.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.wishes_id_seq',
                         (SELECT MAX(id)+1 FROM Wishes),
                         false);