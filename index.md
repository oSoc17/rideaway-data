# The OSM Brussels Cycling Route Validation Tool
<img src="/images/bikeaway%20data%20logo.png" width="200">

## Introducing the Brussels bike data team
During the month of July 2017 three students, guided by expert coaches, worked on an OpenStreetMap (OSM) focused project. The result of is a web tool that supports the Belgian OSM community by assisting them to identify missing map data on the regional cycling network of Brussels. 

## Our end goal: supporting Brussels bike data completeness and correctness on OSM 

- Comparing Brussels’ government reference cycling network open data with OSM
- Visually presenting areas in OSM that doesn’t match to the Brussels data on an interactive and dynamic website

The open Summer of code, an initiative of Open Knowledge Belgium, is a one-month programme which gives technology, design, and communications students the chance to transform open innovation projects into real-world applications. At the 7th edition of oSoc a total of 40 students are working on 10 cutting-edge projects build on open source cod

## The Brussels regional bike network
Brussels have has developed region wide cycling network. Known as the ICR (Itinéraires Cyclables Régionaux) in French or the GFR (Gewestelijke Fietsroutes) in Dutch, the network aims for fluid and safe journeys spanning all 19 communes of the region.To encourage more cyclists on more efficient and safer routes, one approach is to ensure that traveller information is robust enough to guide cyclists to these routes. 

## The need for a dedicated cycling smartphone app for Brussels
Nowadays most people use their phone to route themselves while their driving or using public transport. These apps usually incorporate the signage that travellers will see in their surrounding environment. The #oSoc Bike for Brussels team are pursuing this same strategy. This means that cyclists can better situate themselves in relation to signage.

The development of the app demonstrates the power of high quality open data and would inspire the creation of other advanced apps for the public to support them through everyday activities. This work highlights the importance of supporting open map data creators to support open source applications. 

OSM as the source of map data for the app
For the app to work having an open map data source geodata of the routes is first necessary. This is where our work becomes relevant, since the map data from OSM needs to be complete and accurate in relation to the physical network’s signage.


## Using Brussels’ map data as a reference
On top of the regional cycling infrastructure there is open and online data of routes. Individual routes has information about their corresponding route colour and name. This is a useful reference, however if the OSM community wanted to compare their data with the Brussels reference map, this will not be too easy for them. 

We solved this problem by creating a continuously refreshing platform that automatically identifies potential issues on OSM, in relation to the cycling route map data from the Brussels government. The aim of the online platform is for OSM map editors to simply compare reference geodata to guide their editing in OSM manually.  The technical underpinning of the verification allows two main approaches on analysis of data per individual route:

- Identifying geometric conflicts of issues of general overlap when the OSM data does not match the Brussels data, and vice-versa;
- Identifying possible misplaced attribute data known as tags in the OSM data, including route code and colour, network name, and the operator of the route.

The image below provides an example of all the cycling routes and routes that are apparently missing in OSM. Apart from this visual aid, the website provides more technical information, such as tagging issues, and also an option to download geojsons of routes.  
 
<img src="/images/osm%20brussels%20data%20comparsion.gif?raw=true">

## Using the OSM-Brussels data comparison tool 
Our web tool is intended for advanced OSM editors who are highly verse with editing route relations with JOSM. Therefore any work should be done through collaboration through experts within community should be done. You can make contact with community via:

- mailto:community@osm.be

In summary, the tool that we are developing aims to assist and encourage the verification of the OSM cycling routes in Brussels. Because we are an open source project, the code can be reused for other situations all over the world when one geodataset needs to be used as a reference to compare OSM geodata for completeness and correctness. The open source approach also extend to our collaborating team mates who are working on an mobile web app that uses the route coding and colouring scheme in their routing interface. 
