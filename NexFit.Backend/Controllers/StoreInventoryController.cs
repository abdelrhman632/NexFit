using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Data;
using NexFit.Backend.Models.StoreInventory;

namespace NexFit.Backend.Controllers;

[ApiController]
[Route("api/[controller]")]
public class StoreInventoryController : ControllerBase
{
    private readonly NexFitDbContext _context;

    public StoreInventoryController(NexFitDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<IActionResult> GetStoreInventories()
    {
        var inventories = await _context.StoreInventories.ToListAsync();

        return Ok(inventories);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetStoreInventory(int id)
    {
        var inventory = await _context.StoreInventories
            .FirstOrDefaultAsync(si => si.InventoryID == id);

        if (inventory == null)
        {
            return NotFound(new
            {
                message = $"Store Inventory with ID {id} was not found."
            });
        }

        return Ok(inventory);
    }
    [HttpPost]
    public async Task<IActionResult> CreateStoreInventory([FromBody] StoreInventory inventory)
    {
        if (inventory == null)
        {
            return BadRequest(new
            {
                message = "Store Inventory data is required."
            });
        }

        var branchExists = await _context.Branches
            .AnyAsync(b => b.BranchID == inventory.BranchID);

        if (!branchExists)
        {
            return BadRequest(new
            {
                message = $"Branch with ID {inventory.BranchID} does not exist."
            });
        }

        var productExists = await _context.Products
            .AnyAsync(p => p.ProductID == inventory.ProductID);

        if (!productExists)
        {
            return BadRequest(new
            {
                message = $"Product with ID {inventory.ProductID} does not exist."
            });
        }

        _context.StoreInventories.Add(inventory);
        await _context.SaveChangesAsync();

        return CreatedAtAction(
            nameof(GetStoreInventory),
            new { id = inventory.InventoryID },
            inventory
        );
    }
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateStoreInventory(
    int id,
    [FromBody] StoreInventory inventory)
    {
        if (inventory == null)
        {
            return BadRequest(new
            {
                message = "Inventory data is required."
            });
        }

        var existingInventory = await _context.StoreInventories
            .FindAsync(id);

        if (existingInventory == null)
        {
            return NotFound(new
            {
                message = $"Store inventory with ID {id} was not found."
            });
        }

        var branchExists = await _context.Branches
            .AnyAsync(b => b.BranchID == inventory.BranchID);

        if (!branchExists)
        {
            return BadRequest(new
            {
                message = $"Branch with ID {inventory.BranchID} does not exist."
            });
        }

        var productExists = await _context.Products
            .AnyAsync(p => p.ProductID == inventory.ProductID);

        if (!productExists)
        {
            return BadRequest(new
            {
                message = $"Product with ID {inventory.ProductID} does not exist."
            });
        }

        existingInventory.BranchID = inventory.BranchID;
        existingInventory.ProductID = inventory.ProductID;
        existingInventory.ProductSize = inventory.ProductSize;
        existingInventory.ProductColor = inventory.ProductColor;
        existingInventory.Quantity = inventory.Quantity;
        existingInventory.LastUpdated = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        return Ok(existingInventory);
    }
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteStoreInventory(int id)
    {
        var inventory = await _context.StoreInventories
            .FindAsync(id);

        if (inventory == null)
        {
            return NotFound(new
            {
                message = $"Store inventory with ID {id} was not found."
            });
        }

        _context.StoreInventories.Remove(inventory);

        await _context.SaveChangesAsync();

        return NoContent();
    }
}