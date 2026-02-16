using Backend.Application.Interface;
using Backend.Infrastructure.Service.Mesh;
using Microsoft.Extensions.DependencyInjection;

namespace Backend.Infrastructure.DependencyInjection;

public static class ServiceDI
{
    public static IServiceCollection AddInfrastructureServices(this IServiceCollection services)
    {
        services.AddHttpClient();

        services.AddScoped<IMeshLibMeshService, MeshLibMeshService>();

        return services;
    }
}
