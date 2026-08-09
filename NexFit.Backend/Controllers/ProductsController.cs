using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Data;
using NexFit.Backend.Models.Products;
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
    [HttpPost]
    public async Task<IActionResult> CreateProduct([FromBody] Product product)
    {
        if (product == null)
        {
            return BadRequest(new { message = "Product data is required." });
        }

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        return CreatedAtAction(
            nameof(GetProduct),
            new { id = product.ProductID },
            product
        );
    }
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateProduct(
    int id,
    [FromBody] Product product)
    {
        if (product == null)
        {
            return BadRequest(new
            {
                message = "Invalid product data."
            });
        }

        var existingProduct = await _context.Products
            .FirstOrDefaultAsync(p => p.ProductID == id);

        if (existingProduct == null)
        {
            return NotFound(new
            {
                message = $"Product with ID {id} was not found."
            });
        }

        existingProduct.ProductName = product.ProductName;
        existingProduct.ProductBrand = product.ProductBrand;
        existingProduct.ProductModel = product.ProductModel;
        existingProduct.ProductSKU = product.ProductSKU;
        existingProduct.ProductCategory = product.ProductCategory;
        existingProduct.ProductGender = product.ProductGender;
        existingProduct.ProductPrice = product.ProductPrice;
        existingProduct.ProductMaterial = product.ProductMaterial;
        existingProduct.ProductUsage = product.ProductUsage;
        existingProduct.ProductSurface = product.ProductSurface;
        existingProduct.ProductSupportType = product.ProductSupportType;
        existingProduct.ProductCushioning = product.ProductCushioning;
        existingProduct.ProductBreathability = product.ProductBreathability;
        existingProduct.ProductWeight = product.ProductWeight;
        existingProduct.ProductWaterproof = product.ProductWaterproof;
        existingProduct.ProductDescription = product.ProductDescription;
        existingProduct.RecommendedDistance = product.RecommendedDistance;
        existingProduct.ArchType = product.ArchType;
        existingProduct.FootStrike = product.FootStrike;
        existingProduct.EnergyReturn = product.EnergyReturn;
        existingProduct.ReleaseYear = product.ReleaseYear;
        existingProduct.HeelDropMM = product.HeelDropMM;
        existingProduct.Terrain = product.Terrain;

        await _context.SaveChangesAsync();

        return Ok(existingProduct);
    }
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteProduct(int id)
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

        _context.Products.Remove(product);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}