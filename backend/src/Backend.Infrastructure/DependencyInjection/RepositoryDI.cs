using Microsoft.Extensions.DependencyInjection;

namespace Backend.Infrastructure.DependencyInjection;

public static class RepositoryDI
{
    public static IServiceCollection AddInfrastructureRepositories(this IServiceCollection services)
    {
        return services;
    }
}
