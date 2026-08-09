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
            return BadRequest(new { message = "Store Inventory data is required." });
        }

        _context.StoreInventories.Add(inventory);
        await _context.SaveChangesAsync();

        return CreatedAtAction(
            nameof(GetStoreInventory),
            new { id = inventory.InventoryID },
            inventory
        );
    }
}