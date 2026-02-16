using Microsoft.EntityFrameworkCore;

namespace Backend.Infrastructure.Persistence;

public sealed class BackendDbContext(DbContextOptions<BackendDbContext> options) : DbContext(options)
{
}
