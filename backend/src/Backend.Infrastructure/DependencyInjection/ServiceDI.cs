using Microsoft.Extensions.DependencyInjection;

namespace Backend.Infrastructure.DependencyInjection;

public static class ServiceDI
{
    public static IServiceCollection AddInfrastructureServices(this IServiceCollection services)
    {
        services.AddHttpClient();
        return services;
    }
}
