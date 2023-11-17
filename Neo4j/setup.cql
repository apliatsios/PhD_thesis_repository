// Managing Users in Neo4j
// Create new user
create user <username>
set plaintext password 'password' change required
// Listing current user
SHOW CURRENT USER
// Listing users
SHOW USERS

// Create uniqueness constraint
CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;
// Setting the configuration of the graph
call n10s.graphconfig.init({handleVocabUris:"IGNORE"});
// Remove graph configuration
CALL n10s.graphconfig.drop
// Current setup listed
call n10s.graphconfig.show

// Importing RDF Data
CALL n10s.onto.import.fetch("file:/usr/share/SSNT_ontology_version1_DL.owl","RDF/XML")

//QUERIES
// Return all entities
call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node return node, node.uri as uri, labels(node) as categories

// Neomap: Return all IoT_Entities with their geolocation
match (a:IoT_Entity)-[:hasLocation]->(b:Location) 
return a.name as tooltip, avg(b.lat) as latitude, avg(b.long) as longitude

// Neomap: Return all OpenData_Entities with their geolocation
match (a:OpenData_Entity)-[:hasLocation]->(b:Location) 
return a.name as tooltip, avg(b.lat) as latitude, avg(b.long) as longitude

with {name:'start_point',latitude: 36.96413219670586, longitude: 26.952653220606674} as start_point
with start_point,{name:'end_point',latitude: 36.95606182636865, longitude: 26.944238571498488} as end_point
with [start_point,end_point] as se
unwind se as points
return points.name as tooltip, points.latitude as latitude, points.longitude as longitude


// Return all Entities, Measurements, values for the last hour
with localdatetime({timezone: 'Europe/Athens'}) as now
match (a:IoT_Entity)-[:hasSensor]-(b:Sensor)-[:hasSensorProperty]-(c:SensorProperty{name:"no2"})
where LocalDateTime(c.timestamp) >= now-duration({hours:1}) 
return a.name as IoT_Node, c.name as meausement, c.value as value, c.timestamp as tm

// APOC Custom functions for Air Quality Index Calculations
CALL apoc.custom.declareFunction(
  'aqi_pm2_5(value::NUMBER) :: INT',
  '
    RETURN CASE
    WHEN ($value >= 0 AND $value < 10)  THEN 0
    WHEN ($value >= 10 AND $value < 20) THEN 1
    WHEN ($value >= 20 AND $value < 25) THEN 2
    WHEN ($value >= 25 AND $value < 50) THEN 3
    WHEN ($value >= 50 AND $value < 75) THEN 4
    WHEN ($value >= 75 AND $value < 800) THEN 5
    ELSE -1
  END
  '
);

CALL apoc.custom.declareFunction(
  'aqi_pm10(value::NUMBER) :: INT',
  '
    RETURN CASE
    WHEN ($value >= 0 AND $value < 20)  THEN 0
    WHEN ($value >= 20 AND $value < 40) THEN 1
    WHEN ($value >= 40 AND $value < 50) THEN 2
    WHEN ($value >= 50 AND $value < 100) THEN 3
    WHEN ($value >= 100 AND $value < 150) THEN 4
    WHEN ($value >= 150 AND $value < 1200) THEN 5
    ELSE -1
  END
  '
);

CALL apoc.custom.declareFunction(
  'aqi_so2(value::NUMBER) :: INT',
  '
    RETURN CASE
    WHEN ($value >= 0 AND $value < 100) THEN 0
    WHEN ($value >= 100 AND $value < 200) THEN 1
    WHEN ($value >= 200 AND $value < 350) THEN 2
    WHEN ($value >= 350 AND $value < 500) THEN 3
    WHEN ($value >= 500 AND $value < 750) THEN 4
    WHEN ($value >= 750 AND $value < 1250) THEN 5
    ELSE -1
  END
  '
);

CALL apoc.custom.declareFunction(
  'aqi_no2(value::NUMBER) :: INT',
  '
    RETURN CASE
    WHEN ($value >= 0 AND $value < 40) THEN 0
    WHEN ($value >= 40 AND $value < 90) THEN 1
    WHEN ($value >= 90 AND $value < 120) THEN 2
    WHEN ($value >= 120 AND $value < 230) THEN 3
    WHEN ($value >= 230 AND $value < 340) THEN 4
    WHEN ($value >= 340 AND $value < 1000) THEN 5
    ELSE -1
  END
  '
);

CALL apoc.custom.declareFunction(
  'aqi_o3(value::NUMBER) :: INT', 
  '
    RETURN CASE
    WHEN ($value >= 0 AND $value < 50)  THEN 0
    WHEN ($value >= 50 AND $value < 100) THEN 1
    WHEN ($value >= 100 AND $value < 130) THEN 2
    WHEN ($value >= 130 AND $value < 240) THEN 3
    WHEN ($value >= 240 AND $value < 380) THEN 4
    WHEN ($value >= 380 AND $value < 800) THEN 5
    ELSE -1
  END
  '
);

CALL apoc.custom.declareFunction(
  'AQI(pollutant::STRING, value::NUMBER) :: STRING',
  '
    RETURN CASE
    WHEN $pollutant = "pm2.5" THEN custom.aqi_pm2_5($value)
    WHEN $pollutant = "pm10" THEN custom.aqi_pm10($value)
    WHEN $pollutant = "so2" THEN custom.aqi_so2($value)
    WHEN $pollutant = "no2" THEN custom.aqi_no2($value)
    WHEN $pollutant = "o3" THEN custom.aqi_o3($value)
  END          
  '
);

with ["no2","so2","o3"] as SP_List
unwind SP_List as SP_name
with SP_name, localdatetime({timezone: 'Europe/Athens'}) as now
match (a:IoT_Entity)-[:hasSensor]-(b:Sensor)-[:hasSensorProperty]-(c:SensorProperty{name:SP_name})
where LocalDateTime(c.timestamp) >= now-duration({hours:1}) 
return a.name as IoT_Node, c.name as meausement, avg(c.value) as value , custom.AQI(c.name,avg(c.value)) order by IoT_Node

// Return IoT Entities 
with ["no2","so2","o3"] as SP_List,["pm2.5","pm10"] as PART_List
unwind SP_List as SP_name
unwind PART_List as PART_name
with SP_name,PART_name,localdatetime({timezone: 'Europe/Athens'}) as now
match (a:IoT_Entity)-[:hasSensor]-(b:Sensor)-[:hasSensorProperty]-(c:SensorProperty)
where ((c.name = SP_name) AND (LocalDateTime(c.timestamp) >= now-duration({hours:1}))) or ((c.name = PART_name) AND (LocalDateTime(c.timestamp) >= now-duration({hours:24})))
with a.name as IoT_Node, c.name as measurement, avg(c.value) as value , custom.AQI(c.name,avg(c.value)) as measurement_AQI,["Good","Fair","Moderate","Poor","Very Poor","Extremely Poor"] as AQI_Index 
return IoT_Node, collect(measurement), AQI_Index[max(measurement_AQI)] 


call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
with distinct labels(node) as labels,["no2","so2","o3"] as SP_List,["pm2.5","pm10"] as PART_List
unwind labels as label
unwind SP_List as SP_name
unwind PART_List as PART_name
with SP_name,PART_name,label,localdatetime({timezone: 'Europe/Athens'}) as now
match (a)-[r*1..2]->(b:SensorProperty)
where (label in LABELS(a)) AND (((b.name = SP_name) AND (LocalDateTime(b.timestamp) >= now-duration({hours:1}))) or ((b.name = PART_name) AND (LocalDateTime(b.timestamp) >= now-duration({hours:24}))))
with distinct a.name as Entity, b.name as measurement, avg(b.value) as value , custom.AQI(b.name,avg(b.value)) as measurement_AQI,["Good","Fair","Moderate","Poor","Very Poor","Extremely Poor"] as AQI_Index 
return Entity, collect(measurement), AQI_Index[max(measurement_AQI)]

// call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
// match(node)-[:hasLocation]-(b:Location) 
// WITH distinct point({latitude: 36.95692683880548, longitude: 26.972596966494535}) AS my_position,node,point({latitude: avg(b.lat), longitude: avg(b.long)}) as entity_point
// return node.name, distance(entity_point,my_position) as distance order by distance LIMIT 1

with point({latitude: 36.96413219670586, longitude: 26.952653220606674}) AS start_point, point({latitude: 36.95530873325873,longitude: 26.976775119232496}) AS end_point
with [start_point,end_point] as se
unwind se as points
call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
match(node)-[:hasLocation]-(b:Location) 
with node,point({latitude: avg(b.lat), longitude: avg(b.long)}) as entity_point,points,se
with node, points,distance(entity_point,points) as dist order by dist
return points, collect(node)[0].name, collect(dist)[0]

with point({latitude: 36.96413219670586, longitude: 26.952653220606674}) AS start_point, point({latitude: 36.95530873325873,longitude: 26.976775119232496}) AS end_point
with [start_point,end_point] as se
unwind se as points
call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
match(node)-[:hasLocation]-(b:Location) 
with node,point({latitude: avg(b.lat), longitude: avg(b.long)}) as entity_point,points,se
with node, points,distance(entity_point,points) as dist order by dist
return points, collect(node)[0].name, collect(dist)[0]

call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
with distinct labels(node) as labels,["no2","so2","o3"] as SP_List,["pm2.5","pm10"] as PART_List
unwind labels as label
unwind SP_List as SP_name
unwind PART_List as PART_name
with SP_name,PART_name,label,localdatetime({timezone: 'Europe/Athens'}) as now
match (a)-[r*1..2]->(b:SensorProperty)
where (label in LABELS(a)) AND (((b.name = SP_name) AND (LocalDateTime(b.timestamp) >= now-duration({hours:1}))) or ((b.name = PART_name) AND (LocalDateTime(b.timestamp) >= now-duration({hours:24}))))
with distinct a.name as Entity, b.name as measurement, avg(b.value) as value , custom.AQI(b.name,avg(b.value)) as measurement_AQI,["Good","Fair","Moderate","Poor","Very Poor","Extremely Poor"] as AQI_Index 
return Entity, collect(measurement), AQI_Index[max(measurement_AQI)]


// Neomap
call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
match (node)-[:hasLocation]-(b:Location) 
return {id:node.name,label:node.label,point:point({latitude:avg(b.lat),longitude:avg(b.long)})}

// Query: Geopoints, pollutants, AQI (For Application)

:params 
{
  "SP_List": ["no2","so2","o3"],
  "PART_List": ["pm2.5","pm10"],
  "AQI_Values": ["Good","Fair","Moderate","Poor","Very Poor","Extremely Poor"]
}

call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
match (node)-[:hasLocation]-(l:Location)
unwind labels(node) as label
with collect(distinct label) as labels, localdatetime({timezone: 'Europe/Athens'}) as now,avg(l.lat) as lat, avg(l.long) as long
match (a)-[:hasSensor*0..1]-()-[:hasSensorProperty]->(b:SensorProperty)
where any(i in labels where i in labels(a))
AND (((b.name in $SP_List) AND (LocalDateTime(b.timestamp) >= now-duration({hours:1}))) or ((b.name in $PART_List) AND (LocalDateTime(b.timestamp) >= now-duration({hours:24}))))
with lat,long,a.name as Entity, b.name as measurement, avg(b.value) as value
with lat,long,Entity,apoc.map.fromValues([measurement, round(value, 2, 'CEILING')]) as pollutants, custom.AQI(measurement, value) as measurement_AQI
return {name:Entity, point:{lat:lat, long:long}, pollutants:collect(pollutants),AQI:$AQI_Values[max(measurement_AQI)]}


// Query: Find coLocation
//delete all previous coLocation relationships
optional match ()-[r:coLocation]-()
delete r
with *
//match all entities (IoT_Entities, OpenData_Entities)
call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node
//calculate and collect point for each entity 
match(node)-[:hasLocation]-(b:Location) 
with node, point({latitude: avg(b.lat), longitude: avg(b.long)}) as entity_point
with collect({id:id(node),name:node.name, point: entity_point}) as points
//duplicate unwind points
unwind points as a
unwind points as b
//Calculate distance between nodes
with a, b where a.name <> b.name
with a, b, distance(a.point, b.point) as distance order by distance
with a, collect({id:b.id,name:b.name,weight:distance})[..4] as otherNodes
unwind otherNodes as on
with a, on  
match (m),(n) where id(m)=a.id and id(n)=on.id and m<>n and id(m)<id(n)
create (m)-[r:coLocation{weight:on.weight}]->(n)
return m,r,n

//Query: ShortestPath Unweighted
with point({latitude: 36.96413219670586, longitude: 26.952653220606674}) AS start_point, point({latitude: 36.95530873325873,longitude: 26.976775119232496}) AS end_point
with [start_point,end_point] as se
unwind se as points
call n10s.inference.nodesLabelled('Entity', {catNameProp: "label", catLabel: "Resource", subCatRel: "SCO" }) YIELD node 
match(node)-[:hasLocation]-(b:Location) 
with node,point({latitude: avg(b.lat), longitude: avg(b.long)}) as entity_point,points,se
with node, entity_point, points,distance(entity_point,points) as dist order by dist
with points, collect(node)[0] as edge_nodes
with collect(edge_nodes) as edge
with edge[0] as start_node, edge[1] as end_node
MATCH p = shortestPath((start_node)-[*..15]-(end_node)) 
RETURN p

//==========================NEW===============================================
// Query: Geopoints, pollutants, AQI (For Application)

:params 
{
  "SP_List": ["no2","so2","o3"],
  "PART_List": ["pm2.5","pm10"],
  "AQI_Values": ["Good","Fair","Moderate","Poor","Very Poor","Extremely Poor"]
}

call n10s.inference.nodesLabelled('Entity', {catNameProp: 'label', catLabel: 'Resource', subCatRel: 'SCO' }) YIELD node 
match (node)-[:hasLocation]-(l:Location)
with node,avg(l.lat) as lat, avg(l.long) as long
with node, lat,long,localdatetime({timezone: 'Europe/Athens'}) as now
match (node)-[:hasSensor*0..1]-()-[:hasSensorProperty]->(b:SensorProperty)
where (((b.name in $SP_List) AND (LocalDateTime(b.timestamp) >= now-duration({hours:1}))) or ((b.name in $PART_List) AND (LocalDateTime(b.timestamp) >= now-duration({hours:24}))))
with lat,long, id(node) as id, node.name as Entity, b.name as pollutant, avg(b.value) as value
with lat,long, id, Entity, pollutant, value, toInteger(custom.AQI(pollutant, value)) as aqi_idx
with lat,long, id, Entity,aqi_idx, collect({pollutant:pollutant, pol_aqi:$AQI_Values[aqi_idx], value:round(value, 2, 'CEILING')}) as pol
unwind pol as pollutants
return {name:Entity, point:{lat:lat,long:long},aqi:$AQI_Values[max(aqi_idx)], pollutants:collect(pollutants)}

:params 
{
  "SP_List": ["no2","so2","o3"],
  "PART_List": ["pm2.5","pm10"],
  "AQI_Values": ["Good","Fair","Moderate","Poor","Very Poor","Extremely Poor"],
  "proper_aqi": ["Good","Fair","Moderate","Poor"],
  "start_point": {latitude: 36.96413219670586, longitude: 26.952653220606674},
  "end_point": {latitude: 36.95530873325873, longitude: 26.976775119232496}
}
// Return path
//Delete previous coLocation Relatioships
profile optional match ()-[r:coLocation]-()
delete r
with *
//Find Entities with proper AQI
call n10s.inference.nodesLabelled('Entity', {catNameProp: 'label', catLabel: 'Resource', subCatRel: 'SCO' }) YIELD node 
match (node)-[:hasLocation]-(l:Location)
with node,avg(l.lat) as lat, avg(l.long) as long
with node, lat,long,localdatetime({timezone: 'Europe/Athens'}) as now
match (node)-[:hasSensor*0..1]-()-[:hasSensorProperty]->(b:SensorProperty)
where (((b.name in $SP_List) AND (LocalDateTime(b.timestamp) >= now-duration({hours:1}))) or ((b.name in $PART_List) AND (LocalDateTime(b.timestamp) >= now-duration({hours:24}))))
with lat,long, id(node) as id, node.name as Entity, b.name as pollutant, avg(b.value) as value
with lat,long, id, Entity, pollutant, value, toInteger(custom.AQI(pollutant, value)) as aqi_idx
with lat,long, id, Entity, aqi_idx, collect({pollutant:pollutant, pol_aqi:$AQI_Values[aqi_idx], value:round(value, 2, 'CEILING')}) as pol
unwind pol as pollutants
with {id:id, name:Entity, point:point({latitude:lat,longitude:long}),aqi:$AQI_Values[max(aqi_idx)]} as aqi_points
where aqi_points.aqi in $proper_aqi
with collect({id:aqi_points.id,name:aqi_points.name, point: aqi_points.point}) as points
//duplicate unwind points
unwind points as c
unwind points as d
//Calculate distance between nodes
with c, d where c.name <> d.name
with c, d, distance(c.point, d.point) as distance order by distance
with c, collect({id:d.id,name:d.name,weight:distance})[..4] as otherNodes
unwind otherNodes as on
with c, on  
//Create coLocation Relationships
match (m),(n) where id(m)=c.id and id(n)=on.id and m<>n and id(m)<id(n)
create (m)-[r:coLocation{weight:on.weight}]->(n)
//Remove duplicates ids
with apoc.coll.toSet(collect(id(m))+collect(id(n))) as id_list
//Find the closest node to the starting and ending point
match(z)-[:hasLocation]-(x:Location) where id(z) in id_list
with z,point({latitude: avg(x.lat), longitude: avg(x.long)}) as geo_points
with z,point($start_point) as start_point, point($end_point) as end_point, geo_points
with z,geo_points,[start_point,end_point] as se
unwind se as endpoints
with z,endpoints,distance(geo_points,endpoints) as dist order by dist
with endpoints,collect(z)[0] as edge_nodes
with collect(edge_nodes) as edge
with edge[0] as start_node, edge[1] as end_node
CALL apoc.algo.dijkstra(start_node, end_node, 'coLocation', 'weight') YIELD path, weight
unwind nodes(path) as path_entities
with reverse(collect(path_entities.name)) as path_nodes
match (o)-[:hasLocation]-(p:Location) where o.name in path_nodes
with o,avg(p.lat) as latitude, avg(p.long) as longitude, apoc.coll.indexOf(path_nodes,o.name) as idx
with {idx:idx+1,name:o.name,latitude:latitude,longitude:longitude} as sequence order by idx
return collect(sequence)
