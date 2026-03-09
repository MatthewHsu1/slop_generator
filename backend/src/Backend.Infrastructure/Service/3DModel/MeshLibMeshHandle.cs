using Backend.Application.Interface._3DModel;

namespace Backend.Infrastructure.Service._3DModel
{
    internal class MeshLibMeshHandle : IMeshHandle
    {
        internal MR.Mesh Mesh { get; }

        internal MeshLibMeshHandle(MR.Mesh mesh)
        {
            Mesh = mesh;
        }
    }
}
