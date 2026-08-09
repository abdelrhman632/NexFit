namespace NexFit.Backend.Models.StoreInventory;
using System.ComponentModel.DataAnnotations;
public class StoreInventory
{
    public int InventoryID { get; set; }

    public int BranchID { get; set; }

    public int ProductID { get; set; }
    
[   Range(35, 50, ErrorMessage = "Product size must be between 35 and 50.")]
    public int ProductSize { get; set; }

    public string ProductColor { get; set; } = string.Empty;

    [Range(0, int.MaxValue, ErrorMessage = "Quantity cannot be negative.")]
    public int Quantity { get; set; }
    public DateTime LastUpdated { get; set; } = DateTime.UtcNow;
}
