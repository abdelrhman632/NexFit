using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Data;
using NexFit.Backend.Models;
namespace NexFit.Backend.Controllers;
[ApiController]
[Route("api/[controller]")]
public class BranchesController : ControllerBase
{
    private readonly NexFitDbContext _context;

    public BranchesController(NexFitDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<IActionResult> GetBranches()
    {
        var branches = await _context.Branches.ToListAsync();

        return Ok(branches);
    }


    [HttpGet("{id}")]
    public async Task<IActionResult> GetBranch(int id)
    {
        var branch = await _context.Branches
            .FirstOrDefaultAsync(b => b.BranchID == id);

        if (branch == null)
        {
            return NotFound(new
            {
                message = $"Branch with ID {id} was not found."
            });
        }

        return Ok(branch);
    }

    [HttpPost]
    public async Task<IActionResult> CreateBranch([FromBody] Branch branch)
    {
        if (branch == null)
        {
            return BadRequest(new { message = "Branch data is required." });
        }

        _context.Branches.Add(branch);
        await _context.SaveChangesAsync();

        return CreatedAtAction(
            nameof(GetBranch),
            new { id = branch.BranchID },
            branch
             );
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateBranch(
     int id,
     [FromBody] Branch branch)
    {
        if (branch == null)
        {
            return BadRequest(new { message = "Invalid branch data." });
        }

        var existingBranch = await _context.Branches
            .FirstOrDefaultAsync(b => b.BranchID == id);

        if (existingBranch == null)
        {
            return NotFound(new
            {
                message = $"Branch with ID {id} was not found."
            });
        }

        existingBranch.BranchName = branch.BranchName;
        existingBranch.City = branch.City;
        existingBranch.Address = branch.Address;
        existingBranch.Phone = branch.Phone;
        existingBranch.OpeningHours = branch.OpeningHours;
        existingBranch.IsActive = branch.IsActive;

        await _context.SaveChangesAsync();

        return Ok(existingBranch);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteBranch(int id)
    {
        var branch = await _context.Branches
            .FirstOrDefaultAsync(b => b.BranchID == id);

        if (branch == null)
        {
            return NotFound(new
            {
                message = $"Branch with ID {id} was not found."
            });
        }

        _context.Branches.Remove(branch);
        await _context.SaveChangesAsync();

        return NoContent();
    }
    [HttpGet("{id}/Inventory")]
    public async Task<IActionResult> GetBranchInventory(int id)
    {
        var branch = await _context.Branches
            .FirstOrDefaultAsync(b => b.BranchID == id);

        if (branch == null)
        {
            return NotFound(new
            {
                message = $"Branch with ID {id} was not found."
            });
        }

        var inventory = await _context.StoreInventories
            .Where(i => i.BranchID == id)
            .ToListAsync();

        return Ok(inventory);
    }
}
