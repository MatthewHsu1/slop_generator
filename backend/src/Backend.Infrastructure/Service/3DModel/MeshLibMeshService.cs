using Backend.Application.Interface;
using Backend.Application.Interface._3DModel;
using Backend.Infrastructure.Service._3DModel;
using static MR;

namespace Backend.Infrastructure.Service.Mesh
{
    internal class MeshLibMeshService : IMeshLibMeshService
    {
        /// <summary>
        /// Imports a 3D mesh from a file using MeshLib.
        /// Supports STL, OBJ, PLY and other formats supported by MeshLib.
        /// </summary>
        /// <param name="filePath">Path to the mesh file.</param>
        /// <returns>The loaded MeshLib mesh.</returns>
        public async Task<IMeshHandle> ImportMeshAsync(string filePath, CancellationToken cancellationToken = default)
        {
            cancellationToken.ThrowIfCancellationRequested();

            if (string.IsNullOrWhiteSpace(filePath))
                throw new ArgumentException("File path cannot be null or empty.", nameof(filePath));

            if (!File.Exists(filePath))
                throw new FileNotFoundException("Mesh file not found.", filePath);

            MR.Mesh mesh = MeshLoad.fromAnySupportedFormat(filePath);

            cancellationToken.ThrowIfCancellationRequested();
            return new MeshLibMeshHandle(mesh);
        }
    }
}
