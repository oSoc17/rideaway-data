using NetTopologySuite.Features;
using Newtonsoft.Json;
using System.IO;

namespace NTS_BufferingTest
{
    class Program
    {
        static void Main(string[] args)
        {
            NetTopologySuite.IO.GeoJsonSerializer serialize = new NetTopologySuite.IO.GeoJsonSerializer();
            var inputFile1 = File.OpenText("osm.geojson");
            var inputFile2 = File.OpenText("gfr.geojson");
            var features1 = serialize.Deserialize<FeatureCollection>(new JsonTextReader(inputFile1));
            var features2 = serialize.Deserialize<FeatureCollection>(new JsonTextReader(inputFile2));

            var bufferedFeatures = new FeatureCollection();
            foreach(var feature in features1.Features)
            {
                var op = new NetTopologySuite.Operation.Buffer.BufferOp(feature.Geometry);
                var geometry = op.GetResultGeometry(0.02);

                var bufferedFeature = new Feature(geometry, new AttributesTable());

                bufferedFeatures.Add(bufferedFeature);
            }

            var intersections = new FeatureCollection();
            foreach(var feature in bufferedFeatures.Features)
            {
                foreach(var feature2 in features2.Features)
                {
                    var intersection = feature.Geometry.Intersection(feature2.Geometry);
                    intersections.Add(new Feature(intersection, new AttributesTable()));
                }
            }

            var differences = new FeatureCollection();
            foreach (var feature in bufferedFeatures.Features)
            {
                foreach (var feature2 in features2.Features)
                {
                    var difference = feature.Geometry.Intersection(feature2.Geometry);
                    differences.Add(new Feature(difference, new AttributesTable()));
                }
            }

            File.Delete("buffered.geojson");
            using (var outputFile = new StreamWriter(File.OpenWrite("buffered.geojson")))
            {
                serialize.Serialize(outputFile, bufferedFeatures);
            }
            File.Delete("intersections.geojson");
            using (var outputFile = new StreamWriter(File.OpenWrite("intersections.geojson")))
            {
                serialize.Serialize(outputFile, intersections);
            }
            File.Delete("differences.geojson");
            using (var outputFile = new StreamWriter(File.OpenWrite("differences.geojson")))
            {
                serialize.Serialize(outputFile, differences);
            }
        }
    }
}
