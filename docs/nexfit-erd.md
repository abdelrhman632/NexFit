# NexFit ERD

## Overview

This diagram shows the core relational structure of the NexFit database.

## Entities

### Branches
- BranchID (PK)
- BranchName
- City
- Address
- Phone
- OpeningHours
- IsActive

### Products
- ProductID (PK)
- ProductName
- ProductBrand
- ProductModel
- ProductSKU
- ProductCategory
- ProductGender
- ProductPrice
- ProductMaterial
- ProductUsage
- ProductSurface
- ProductSupportType
- ProductCushioning
- ProductBreathability
- ProductWeight
- ProductWaterProof
- ProductDescription
- ArchType
- FootStrike
- EnergyReturn
- ReleaseYear
- HeelDropMM
- Terrain

### StoreInventory
- InventoryID (PK)
- BranchID (FK)
- ProductID (FK)
- ProductSize
- ProductColor
- Quantity
- LastUpdated

## Relationships

- One Branch has many StoreInventory records.
- One Product has many StoreInventory records.
- StoreInventory acts as the junction table between Branches and Products.

## Notes

The ERD is maintained in draw.io and exported for repository documentation.
