using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Backend.Infrastructure.DependencyInjection;

public static class InfrastructureDI
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddInfrastructureServices();
        services.AddInfrastructureRepositories();
        services.AddInfrastructureOptions(configuration);
        services.AddInfrastructureCaching(configuration);
        services.AddAppDbContext(configuration);
        services.AddInfrastructureRateLimiting();

        return services;
    }
}
