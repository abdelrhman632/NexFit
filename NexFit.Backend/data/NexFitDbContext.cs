using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Models;
using NexFit.Backend.Models.Products;  
using NexFit.Backend.Models.StoreInventory; 
namespace NexFit.Backend.Data;

public class NexFitDbContext : DbContext
{
    public NexFitDbContext(DbContextOptions<NexFitDbContext> options)
        : base(options)
    {
    }

    public DbSet<Branch> Branches { get; set; }
    public DbSet<Product> Products { get; set; }
    public DbSet<StoreInventory> StoreInventories { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Branch>(entity =>
        {
            entity.ToTable("branches");

            entity.HasKey(b => b.BranchID);

            entity.Property(b => b.BranchID)
                .HasColumnName("branchid");

            entity.Property(b => b.BranchName)
                .HasColumnName("branchname");

            entity.Property(b => b.City)
                .HasColumnName("city");

            entity.Property(b => b.Address)
                .HasColumnName("address");

            entity.Property(b => b.Phone)
                .HasColumnName("phone");

            entity.Property(b => b.OpeningHours)
                .HasColumnName("openinghours");

            entity.Property(b => b.IsActive)
                .HasColumnName("isactive");
        });
         modelBuilder.Entity<Product>(entity =>
        {
            entity.ToTable("products");

            entity.HasKey(p => p.ProductID);

            entity.Property(p => p.ProductID)
                .HasColumnName("productid");

            entity.Property(p => p.ProductName)
                .HasColumnName("productname");

            entity.Property(p => p.ProductBrand)
                .HasColumnName("productbrand");

            entity.Property(p => p.ProductModel)
                .HasColumnName("productmodel");

            entity.Property(p => p.ProductSKU)
                .HasColumnName("productsku");

            entity.Property(p => p.ProductCategory)
                .HasColumnName("productcategory");

            entity.Property(p => p.ProductGender)
                .HasColumnName("productgender");

            entity.Property(p => p.ProductPrice)
                .HasColumnName("productprice");

            entity.Property(p => p.ProductMaterial)
                .HasColumnName("productmaterial");

            entity.Property(p => p.ProductUsage)
                .HasColumnName("productusage");

            entity.Property(p => p.ProductSurface)
                .HasColumnName("productsurface");

            entity.Property(p => p.ProductSupportType)
                .HasColumnName("productsupporttype");

            entity.Property(p => p.ProductCushioning)
                .HasColumnName("productcushioning");

            entity.Property(p => p.ProductBreathability)
                .HasColumnName("productbreathability");

            entity.Property(p => p.ProductWeight)
                .HasColumnName("productweight");

            entity.Property(p => p.ProductWaterproof)
                .HasColumnName("productwaterproof");

            entity.Property(p => p.ProductDescription)
                .HasColumnName("productdescription");

            entity.Property(p => p.RecommendedDistance)
                .HasColumnName("recommendeddistance");

            entity.Property(p => p.ArchType)
                .HasColumnName("archtype");

            entity.Property(p => p.FootStrike)
                .HasColumnName("footstrike");

            entity.Property(p => p.EnergyReturn)
                .HasColumnName("energyreturn");

            entity.Property(p => p.ReleaseYear)
                .HasColumnName("releaseyear");

            entity.Property(p => p.HeelDropMM)
                .HasColumnName("heeldropmm");

            entity.Property(p => p.Terrain)
                .HasColumnName("terrain");
        });
        modelBuilder.Entity<StoreInventory>(entity =>
        {
            entity.ToTable("storeinventory");

            entity.HasKey(si => si.InventoryID);

            entity.Property(si => si.InventoryID)
                .HasColumnName("inventoryid");

            entity.Property(si => si.BranchID)
                .HasColumnName("branchid");

            entity.Property(si => si.ProductID)
                .HasColumnName("productid");
            
            entity.Property(si => si.ProductSize)
                .HasColumnName("productsize");
                
            entity.Property(si => si.ProductColor)
                .HasColumnName("productcolor");

            entity.Property(si => si.Quantity)
                .HasColumnName("quantity");

            entity.Property(si => si.LastUpdated)
                .HasColumnName("lastupdated");
        });
    }
}
