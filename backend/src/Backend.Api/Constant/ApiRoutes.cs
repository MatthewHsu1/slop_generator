namespace Backend.Api.Constant
{
    public class ApiRoutes
    {
        public const string Base = "api";

        public static class ThreeDModel
        {
            public const string Segment = "3D";

            public const string Endpoint = "import";

            public const string ImportFull = Base + "/" + Segment + "/" + Endpoint;
        }
    }
}
