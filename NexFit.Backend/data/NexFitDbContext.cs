using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Models;

namespace NexFit.Backend.Data;

public class NexFitDbContext : DbContext
{
    public NexFitDbContext(DbContextOptions<NexFitDbContext> options)
        : base(options)
    {
    }

    public DbSet<Branch> Branches { get; set; }

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
    }
}