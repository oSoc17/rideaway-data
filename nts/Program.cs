using NetTopologySuite.Features;
using Newtonsoft.Json;
using System.IO;
using System;

namespace NTS_BufferingTest
{
    class Program
    {
        static void Main(string[] args)
        {
            NetTopologySuite.IO.GeoJsonSerializer serialize = new NetTopologySuite.IO.GeoJsonSerializer();
            var inputFile1 = File.OpenText(args[0]);
            var inputFile2 = File.OpenText(args[1]);
            var features1 = serialize.Deserialize<FeatureCollection>(new JsonTextReader(inputFile1));
            var features2 = serialize.Deserialize<FeatureCollection>(new JsonTextReader(inputFile2));

            var bufferedFeatures = new FeatureCollection();
            foreach(var feature in features1.Features)
            {
                var op = new NetTopologySuite.Operation.Buffer.BufferOp(feature.Geometry);
                var geometry = op.GetResultGeometry(0.0003);

                var bufferedFeature = new Feature(geometry, new AttributesTable());

                bufferedFeatures.Add(bufferedFeature);
            }
            /*
            var intersections = new FeatureCollection();
            foreach(var feature in bufferedFeatures.Features)
            {
                foreach(var feature2 in features2.Features)
                {
                    var intersection = feature.Geometry.Intersection(feature2.Geometry);
                    intersections.Add(new Feature(intersection, new AttributesTable()));
                }
            }
            */
            var differences = new FeatureCollection();
            foreach (var feature in bufferedFeatures.Features)
            {
                foreach (var feature2 in features2.Features)
                {
                    var difference = feature2.Geometry.Difference(feature.Geometry);
                    differences.Add(new Feature(difference, new AttributesTable()));

                    
                }
            }
            // Console.WriteLine(differences.Features.Count.ToString());
            // File.Delete("buffered.geojson");
            // using (var outputFile = new StreamWriter(File.OpenWrite("buffered.geojson")))
            // {
            //    serialize.Serialize(outputFile, bufferedFeatures);
            // }
            // File.Delete(args[2]);
            // using (var outputFile = new StreamWriter(File.OpenWrite(args[2])))
            // {
            //    serialize.Serialize(outputFile, intersections);
            // }
            File.Delete(args[2]);
            using (var outputFile = new StreamWriter(File.OpenWrite(args[3])))
            {
                serialize.Serialize(outputFile, differences);
            }

        }
    }
}
