using Backend.Application.Interface;
using Backend.Application.Interface._3DModel;
using Backend.Infrastructure.Service._3DModel;
using static MR;

namespace Backend.Infrastructure.Service.Mesh
{
    internal class MeshLibMeshService : IMeshLibMeshService
    {
        /// <inheritdoc/>
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
        
        /// <inheritdoc/>
        public async Task<IMeshHandle> ImportMeshAsync(Stream stream, string fileExtension, CancellationToken cancellationToken = default)
        {
            cancellationToken.ThrowIfCancellationRequested();

            if (stream == null || !stream.CanRead)
                throw new ArgumentException("Stream must be readable.", nameof(stream));

            var ext = string.IsNullOrWhiteSpace(fileExtension) ? ".bin"
                : fileExtension.StartsWith('.') ? fileExtension : "." + fileExtension;

            var tempPath = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName() + ext);

            try
            {
                await using (var fileStream = File.Create(tempPath))
                    await stream.CopyToAsync(fileStream, cancellationToken);

                return await ImportMeshAsync(tempPath, cancellationToken);
            }
            finally
            {
                if (File.Exists(tempPath))
                    File.Delete(tempPath);
            }
        }
    }
}
