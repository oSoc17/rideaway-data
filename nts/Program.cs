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
            /*
            3 inputs are required, 2 files to compare and one output
            It compares it geometric overlaap between the first 2 inputs and uses the third for output
            A buffered version of the first input is compared to the second input
            The output is the geometric difference between the inputs 
            */

            var serialize = new NetTopologySuite.IO.GeoJsonSerializer();
            var inputFile1 = File.OpenText(args[0]);
            var inputFile2 = File.OpenText(args[1]);
            var features1 = serialize.Deserialize<FeatureCollection>(new JsonTextReader(inputFile1));
            var features2 = serialize.Deserialize<FeatureCollection>(new JsonTextReader(inputFile2));

            //buffer first input
            var bufferedFeatures = new FeatureCollection();
            foreach(var feature in features1.Features)
            {
                var op = new NetTopologySuite.Operation.Buffer.BufferOp(feature.Geometry);
                var geometry = op.GetResultGeometry(0.0003);

                var bufferedFeature = new Feature(geometry, new AttributesTable());

                bufferedFeatures.Add(bufferedFeature);
            }
            //extract all differences by comparing a feuture from input 1 with all features from input 2
            var differences = new FeatureCollection();
            foreach (var feature in bufferedFeatures.Features)
            {
                foreach (var feature2 in features2.Features)
                {
                    var difference = feature2.Geometry.Difference(feature.Geometry);
                    differences.Add(new Feature(difference, new AttributesTable()));
                }
            }

           //output file created
            File.Delete(args[2]);
            using (var outputFile = new StreamWriter(File.OpenWrite(args[2])))
            {
                serialize.Serialize(outputFile, differences);
            }
        }
    }
}
