namespace NexFit.Backend.Models.StoreInventory;

public class StoreInventory
{
    public int InventoryID { get; set; }

    public int BranchID { get; set; }

    public int ProductID { get; set; }

    public int ProductSize { get; set; }

    public string ProductColor { get; set; } = string.Empty;

    public int Quantity { get; set; }
    public DateTime LastUpdated { get; set; } = DateTime.UtcNow;
}
