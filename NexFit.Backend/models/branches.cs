namespace NexFit.Backend.Models;

public class Branch
{
    public int BranchID { get; set; }

    public string BranchName { get; set; } = string.Empty;

    public string City { get; set; } = string.Empty;

    public string Address { get; set; } = string.Empty;

    public string? Phone { get; set; }

    public string? OpeningHours { get; set; }

    public bool IsActive { get; set; }
}