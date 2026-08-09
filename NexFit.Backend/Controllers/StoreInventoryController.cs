using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Data;

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
}