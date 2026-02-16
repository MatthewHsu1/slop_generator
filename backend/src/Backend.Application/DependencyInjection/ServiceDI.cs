using Microsoft.Extensions.DependencyInjection;

namespace Backend.Application.DependencyInjection;

public static class ServiceDI
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        services.AddSingleton(TimeProvider.System);
        return services;
    }
}
