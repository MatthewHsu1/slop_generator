using Backend.Application.Interface._3DModel;

namespace Backend.Application.Interface
{
    public interface IMeshLibMeshService
    {
        Task<IMeshHandle> ImportMeshAsync(string filePath, CancellationToken cancellationToken = default);
    }
}
