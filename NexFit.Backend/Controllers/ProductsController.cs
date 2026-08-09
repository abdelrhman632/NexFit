using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Data;

namespace NexFit.Backend.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly NexFitDbContext _context;

    public ProductsController(NexFitDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<IActionResult> GetProducts()
    {
        var products = await _context.Products.ToListAsync();

        return Ok(products);
    }
    
    [HttpGet("{id}")]
    public async Task<IActionResult> GetProduct(int id)
    {
        var product = await _context.Products
            .FirstOrDefaultAsync(p => p.ProductID == id);

        if (product == null)
        {
            return NotFound(new
            {
                message = $"Product with ID {id} was not found."
            });
        }

        return Ok(product);
    }
}