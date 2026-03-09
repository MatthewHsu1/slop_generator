using Backend.Api.Constant;
using Backend.Application.Interface;
using Microsoft.AspNetCore.Mvc;

namespace Backend.Api.Controller
{
    [ApiController]
    [Route($"{ApiRoutes.Base}/[controller]")]
    public class ThreeDModelController(IMeshLibMeshService meshLib) : ControllerBase
    {
        [HttpPost(ApiRoutes.ThreeDModel.Endpoint)]
        public async Task<IActionResult> Test(IFormFile file, CancellationToken cancellationToken)
        {
            if (file == null || file.Length == 0)
                return BadRequest("No file uploaded.");

            var extension = Path.GetExtension(file.FileName);
            await using var stream = file.OpenReadStream();

            var result = await meshLib.ImportMeshAsync(stream, extension, cancellationToken);

            return Ok();
        }
    }
}
