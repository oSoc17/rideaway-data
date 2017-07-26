<p align="center">
<img src="./images/bikeaway%20data%20logo.png" width="400">
</p>

## Introducing the Brussels Mobility data team
During the month of July 2017 three students, guided by expert coaches, worked on an OpenStreetMap (OSM) focused project. Our work was done in the context of the 2017 open Summer of code, which is an initiative of Open Knowledge Belgium. The oSoc challenges teams of students to solve real-world problems through application development. At the 7th edition of oSoc, a total of 40 students worked on 10 cutting-edge projects build on open source code.

## The Brussels regional bike network
Brussels have has developed region wide cycling network. Known as the ICR (Itinéraires Cyclables Régionaux) in French or the GFR (Gewestelijke Fietsroutes) in Dutch, the network aims for fluid and safe journeys spanning all 19 communes of the region.To encourage more cyclists on more efficient and safer routes, one approach is to ensure that traveller information is robust enough to guide cyclists to these routes. 

<p align="center">
<img src="./images/brusselsregioncyclingroutes.png" width="500">
</p>

## The Bike for Brussels navigation app
The Brussels cycling network aims to encourage citizens and visitors alike to bike around efficiently and safely on a system designed especially for longer distance cross-regional journeys.The benefits of such a modal-shift, to cycling, are bountiful and there is a drive to have 20% of transport being undertaken by the bike by the year 2020. These wider goals are part of the Bike for Brussels social media awareness campaign.  

### A dedicated cycling app for the Brussels cycling network
Nowadays most people use their phone to route themselves while their driving or using public transport. These apps usually incorporate the signage that travellers will see in their surrounding environment. The #oSoc Bike for Brussels team is pursuing this same strategy. This means that cyclists can better situate themselves in relation to signage.

The development of the app demonstrates the power of high-quality open data and would inspire the creation of other advanced apps for the public to support them through everyday activities. This work highlights the importance of supporting open map data creators to support open source applications. 

## OSM as the source of map data for the cycling app
OSM is a collaborative project to create a free editable map of the world. Mapping is done through local expert knowledge and continually create and validate the map. In Belgium, the local community is very active and this has allowed cycling paths all over the country, especially in urban areas like Brussels, to be mapped with a high level of completeness and correctness. 

OSM is already used by well-known cycling navigation apps like [Strava](https://www.strava.com/) and [CityMapper](https://citymapper.com/) thus illustrates the power of OSM as a reputable source of map data. When OSM Brussels bike data improves, this also benefits other third party data users of OSM to improve the reliability of their applications.

This is where our work becomes relevant since the map data from OSM needs to be complete and accurate for a navigation app for the city to be reliable. We developed an approach available to assist the OSM community to verify that map data is a good quality. Even though mappers usually carry out their work based on personal knowledge, OSM contributors often rely official reference maps on a particular theme to guide their work. When they are issues then they can edit the map to correct for it. Our solution, therefore, ensures the map comparison and correction process, known as conflation, a lot more efficient.

## Using Brussels’ map data as a reference for OSM
The regional cycling infrastructure is represented by is open and online map data. Individual routes have information about their corresponding route colour and name. This is a useful reference, however, if the OSM community wanted to compare the completeness and correctness of OSM, a manual comparison will be too tedious. We solved this problem by providing a platform, to the OSM community, that automatically identifies potential issues on OSM, in relation to the cycling route map data from the Brussels government. 

## A webtool for Brussels OSM bike data completeness and correctness 
The result of our work is a web tool that supports the Belgian OSM community by assisting them to identify missing map data on the regional cycling network of Brussels. The tool, available from this via [cyclenetworks.osm.be](http://cyclenetworks.osm.be/).

The webtool continuously refreshes itself and automatically identifies potential issues on OSM. Map editors can then use the website to guide their editing. The technical underpinning of the verification allows two main approaches to analysis of data per individual route by identifying:

- Geometric conflicts of issues of general overlap when the OSM data does not match the Brussels data, and vice-versa
- Possible misplaced attribute data known as tags in the OSM data, including route code and colour, network name, and the operator of the route

The image below provides an example of all the cycling routes and routes that are apparently missing in OSM. Apart from this visual aid, the website provides more technical information, such as tagging issues, and also an option to download geojsons of routes.  

### An example of potential gaps in OSM compared to Brussels' data
<p align="center">
<img src="./images/osmbrusselsdatacomparsion.gif" width="700">
</p>

### Using the OSM Brussels data validation tool
Our web tool is intended for advanced OSM editors who are highly versed with editing route relations with JOSM. An introduction of the can be viewed from this [link](https://cyclenetworks.osm.be/brumob/about/). However, it is highly recommended that mapping work on the Brussels regional network should be done in collaboration with the OSM Belgium community by making contact with them via community@osm.be

In summary, the tool that we are developing aims to assist and encourage the verification of the OSM cycling routes in Brussels. Because we are an open source project, the code can be reused for other situations all over the world when one geo dataset needs to be used as a reference, to compare OSM geodata for completeness and correctness. The open source approach also extends to our collaborating team mates who are working on a mobile web app that uses the route coding and colouring scheme in their routeing interface. 

## Project team members and contact
- [Ben Abelshausen (team coach and primary contact)](mailto:community@osm.be)
- [Damian Robinson (communication)](https://linkedin.com/in/damiangrobinson)
- [Dieter Debast (developer)](mailto:dieterdebast@outlook.com)
- [Moustapha Ramachi (developer)](mailto:moustapha.ramachi@gmail.com)

## Some useful links
* The OSM cycling data validation web tool for Brussels via [cyclenetworks.osm.be](http://cyclenetworks.osm.be/)
* [An introduction to the validation tool](https://cyclenetworks.osm.be/brumob/about/)
* [open Summer of code](http://2017.summerofcode.be/) (an initiative of [Open Knowledge Belgium](https://www.openknowledge.be/))
* [OpenStreetMap Belgian Community](http://osm.be/)
* Event that was organised within this theme: [Open Bike Data & Mapping with OpenStreetMap](https://www.eventbrite.com/e/open-bike-data-mapping-with-openstreetmap-registration-34806438996)
* The [Brussels government's mobility department](http://mobility.brussels/)
* Info about the [ICR (Itinéraires Cyclables Régionaux)](http://www.bruxellesmobilite.irisnet.be/articles/velo/itineraires-cyclables) in French
* Info about the [GFR (Gewestelijke Fietsroutes)](http://www.mobielbrussel.irisnet.be/articles/fiets/fietsroutes) in Dutch
* Technical guidlines for the ICR-GFR signage in [Dutch](http://www.mobielbrussel.irisnet.be/partners/professionelen/technische-publicaties) and [French](http://www.bruxellesmobilite.irisnet.be/partners/professionnels/publications-techniques)
* The [Bike for Brussels](http://bike.brussels/) social media awareness campaign
* Freely online map [data from the Brussels government](http://data-mobility.brussels/mobigis/nl/)
* [Info on the Java OpenStreetMap Editor (JOSM)](https://josm.openstreetmap.de/)
* OSM wiki on [comparison and quality control](http://wiki.openstreetmap.org/wiki/Comparing_OSM_with_other_datasets)
* OSM wiki on map [conflation](http://wiki.openstreetmap.org/wiki/Conflation)
* [Mapping conventions, including for cycling routes](http://wiki.openstreetmap.org/wiki/WikiProject_Belgium/Conventions/Cycle_Routes) for Belgium
* OSM wiki on the [Brussels Capital Region](http://wiki.openstreetmap.org/wiki/WikiProject_Belgium/Cycle_Routes%23Itin.C3.A9raires_Cyclables_R.C3.A9gionaux_-_Gewestelijke_Fietsroute)
* [The testing version of the Brussels cycling routing webapp](https://osoc17.github.io/rideaway-frontend/)
