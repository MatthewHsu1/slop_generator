using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Backend.Infrastructure.DependencyInjection;

public static class OptionsDI
{
    public static IServiceCollection AddInfrastructureOptions(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services
            .AddOptions<InfrastructureOptions>()
            .Bind(configuration.GetSection(InfrastructureOptions.SectionName));

        return services;
    }
}

public sealed class InfrastructureOptions
{
    public const string SectionName = "Infrastructure";
}
