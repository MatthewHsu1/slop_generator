using Backend.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Backend.Infrastructure.DependencyInjection;

public static class AppDBContextDI
{
    public static IServiceCollection AddAppDbContext(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var connectionString = configuration["ConnectionStrings:DefaultConnection"]
            ?? "Host=localhost;Port=5432;Database=backend;Username=postgres;Password=postgres";

        services.AddDbContext<BackendDbContext>(options => options.UseNpgsql(connectionString));

        return services;
    }
}
