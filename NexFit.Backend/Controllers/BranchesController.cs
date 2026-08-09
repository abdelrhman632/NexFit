using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexFit.Backend.Data;

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
}