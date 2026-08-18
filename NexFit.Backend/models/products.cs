namespace NexFit.Backend.Models.Products;
using System.ComponentModel.DataAnnotations;

public class Product
{
    public int ProductID { get; set; }

    public string ProductName { get; set; } = string.Empty;
    public string ProductBrand { get; set; } = string.Empty;
    public string ProductModel { get; set; } = string.Empty;
    public string ProductSKU { get; set; } = string.Empty;
    public string ProductCategory { get; set; } = string.Empty;
    public string ProductGender { get; set; } = string.Empty;
    
    [Range(0.01, double.MaxValue, ErrorMessage = "Product price must be greater than 0.")]
    public decimal ProductPrice { get; set; }
    
    public string ProductMaterial { get; set; } = string.Empty;
    public string ProductUsage { get; set; } = string.Empty;
    public string ProductSurface { get; set; } = string.Empty;
    public string ProductSupportType { get; set; } = string.Empty;
    public string ProductCushioning { get; set; } = string.Empty;
    public string ProductBreathability { get; set; } = string.Empty;

    public decimal ProductWeight { get; set; }

    public bool ProductWaterproof { get; set; }

    public string ProductDescription { get; set; } = string.Empty;

    public string RecommendedDistance { get; set; } = string.Empty;
    public string ArchType { get; set; } = string.Empty;
    public string FootStrike { get; set; } = string.Empty;
    public string EnergyReturn { get; set; } = string.Empty;

    public int ReleaseYear { get; set; }

    public int HeelDropMM { get; set; }

    public string Terrain { get; set; } = string.Empty;
}