CREATE TABLE StoreInventory (
    InventoryID SERIAL PRIMARY KEY,
    BranchID INT NOT NULL
        REFERENCES Branches(BranchID)
        ON DELETE CASCADE,
    ProductID INT NOT NULL
        REFERENCES Products(ProductID)
        ON DELETE CASCADE,
    ProductSize INT NOT NULL,
    ProductColor VARCHAR(50),
    Quantity INT NOT NULL DEFAULT 0,
    LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);