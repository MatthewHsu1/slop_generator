using Microsoft.Extensions.DependencyInjection;

namespace Backend.Infrastructure.DependencyInjection;

public static class RateLimitingDI
{
    public static IServiceCollection AddInfrastructureRateLimiting(this IServiceCollection services)
    {
        return services;
    }
}
