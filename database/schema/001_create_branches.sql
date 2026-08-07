CREATE TABLE Branches (
    BranchID SERIAL PRIMARY KEY,
    BranchName VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Address TEXT NOT NULL,
    Phone VARCHAR(20),
    OpeningHours VARCHAR(100),
    IsActive BOOLEAN DEFAULT TRUE
);