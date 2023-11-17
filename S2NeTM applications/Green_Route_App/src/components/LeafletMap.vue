<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import 'leaflet-routing-machine'

import HealthWarnings from '../utils/HealthWarnings'
import goodImage from '../assets/img/blue-good.png'
import fairImage from "../assets/img/greenish-fair.png"
import moderateImage from "../assets/img/yellow-moderate.png"
import poorImage from "../assets/img/orange-poor.png"
import veryPoorImage from "../assets/img/red-very-poor.png"
import extremelyPoorImage from "../assets/img/maroon-extremely-poor.png"

export default{
    // name: "LeafletMap",
    props: ['center', 'data', 'points', 'mutationLoading'],
    data(){
        return {
            myMap: null,
            wayPoints: null,
            routingControl: null,
            aqiColorStyle: null,
            tableStart: `<table class="table" style="text-align: center;">
                            <thead class="table-light">
                                <td >A/A</td><td>Όνομα</td><td>Τιμή (μg/m<sup>3</sup>)</td><td>AQI</td>
                            </thead>
                            <tbody>`,
            tableEnd: `</tbody>
                        </table>`
        }
    },
    watch:{
        points(){
            if(this.points.length>0){
                this.loadMap()
            }
        },
        deleteMap(){
            if(this.destroyMap){
                if (this.myMap && this.myMap.remove) {
                    this.myMap.off();
                    this.myMap.remove();
                }
            }
        },
        newRoute(){
            if (this.mutationLoading) {
                if (this.routingControl != null) {
                    this.map.removeControl(this.routingControl);
                    this.routingControl = null;
                }
            }
        }
    },
    methods: {
        onMapClick(e){
            this.$emit('mapclicked', e.latlng)
        },
        pollutantsData(data){
            let html = ''
            html += data.pollutants.map((pollutant, index)=>{
                let ColorStyle =''
                if (pollutant.pol_aqi=='Good') {
                    ColorStyle = 'style-good'
                } else if (pollutant.pol_aqi=='Fair') {
                    ColorStyle = 'style-fair'
                } else if (pollutant.pol_aqi=='Moderate') {
                    ColorStyle = 'style-moderate'
                } else if (pollutant.pol_aqi=='Poor') {
                    ColorStyle = 'style-poor'
                } else if (pollutant.pol_aqi=='Very Poor') {
                    ColorStyle = 'style-very-poor'
                } else if (pollutant.pol_aqi=='Extremely Poor') {
                    ColorStyle = 'style-extremely-poor'
                }
                return `<tr class="${ColorStyle}" >
                            <td>${index+1}</td>    
                            <td>${pollutant.pollutant}</td>
                            <td>${pollutant.value}</td>
                            <td>${pollutant.pol_aqi}</td>
                        </tr>`
            })
            // Έβαζε κόμα μετά από κάθε <tr>, οπότε τα αφαιρούμε
            return html.replace(/,/g, '')
            
        },
        loadMap(){
            if(!this.myMap){
            this.myMap = L.map('mapContainer').setView(this.center, 13)
            this.myMap.options.attributionControl = false
            var LeafIcon = L.Icon.extend({
                options: {
                    iconSize:     [28, 28],
                    iconAnchor:   [22, 22],
                    popupAnchor:  [-3, -26]
                }
            })
            const goodIcon = new LeafIcon({iconUrl: goodImage}),
                  fairIcon = new LeafIcon({iconUrl: fairImage}),
                  moderateIcon = new LeafIcon({iconUrl: moderateImage}),
                  poorIcon = new LeafIcon({iconUrl: poorImage}),
                  veryPoorIcon = new LeafIcon({iconUrl: veryPoorImage}),
                  extremelyPoorIcon = new LeafIcon({iconUrl: extremelyPoorImage})
            const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution:
                '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(this.myMap)
            let ColorStyle = null
            let healthWarningGeneralPopulation = ''
            let healthWarningSensitivePopulation = ''
            for (let entity of this.data) {
                let myIcon
                healthWarningGeneralPopulation   = HealthWarnings.find((warning) => warning.state == entity.aqi).generalPopulation
                healthWarningSensitivePopulation = HealthWarnings.find((warning) => warning.state == entity.aqi).sensitivePopulation
                if (entity.aqi=='Good') {
                    myIcon = goodIcon
                    ColorStyle = 'style-good'
                } else if (entity.aqi=='Fair') {
                    myIcon = fairIcon
                    ColorStyle = 'style-fair'
                } else if (entity.aqi=='Moderate') {
                    myIcon = moderateIcon
                    ColorStyle = 'style-moderate'
                } else if (entity.aqi=='Poor') {
                    myIcon = poorIcon
                    ColorStyle = 'style-poor'
                } else if (entity.aqi=='Very Poor') {
                    myIcon = veryPoorIcon
                    ColorStyle = 'style-very-poor'
                } else if (entity.aqi=='Extremely Poor') {
                    myIcon = extremelyPoorIcon
                    ColorStyle = 'style-extremely-poor'
                }
                 const marker = L.marker([entity.point.lat, entity.point.long], {icon: myIcon})
                .addTo(this.myMap)
                .bindPopup(`<div class="card">
                    <div class="card-header">
                        Σταθμός: <strong>${entity.name}</strong>
                    </div>
                    <div class="card-body">
                        <h4 class="card-title">Δείκτης Ποιότητας Αέρα</h4>
                        
                            <div class="row">
                                <div class="col-xs-12 col-md-12 ${ColorStyle}" style="border: 2px solid; border-radius: 5px; ;">
                                    <h2 style="text-align: center; vertical-align: middle">${entity.aqi}</h2>
                                </div>                        
                        ${this.tableStart}
                        ${this.pollutantsData(entity)}
                        ${this.tableEnd}
                        
                                <div class="col" style="border: 2px solid; border-radius: 5px;">
                                    <h4 class="text-center">Οδηγίες</h4>
                                </div>
                                <div class="accordion" id="accordionExample">
                                <div class="accordion-item">
                                    <h2 class="accordion-header" id="headingOne">
                                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                                        Γενικός Πληθυσμός
                                    </button>
                                    </h2>
                                    <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                                    <div class="accordion-body">
                                        <p>${healthWarningGeneralPopulation}</p>
                                    </div>
                                    </div>
                                </div>
                                <div class="accordion-item">
                                    <h2 class="accordion-header" id="headingTwo">
                                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                        Ευαίσθητες Ομάδες
                                    </button>
                                    </h2>
                                    <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
                                    <div class="accordion-body">
                                        ${healthWarningSensitivePopulation}</div>
                                    </div>
                                </div>
  
                            </div>
                            </div>
                    </div>
                    </div>`)

                
                
            }
            if (this.myMap){
                this.myMap.on('click', this.onMapClick)
            }
        } 
        else {
            if (this.points.length>0) {
                    let myWaypoints = []
                    for (let point of this.points){
                        myWaypoints.push(L.latLng(point.lat, point.long))
                    }
                    if (this.routingControl){
                        this.routingControl.setWaypoints(myWaypoints)
                    }
                    else{

                        this.routingControl = L.Routing.control({
                            waypoints: myWaypoints,
                            createMarker: function(i, wp, n) {
                                // Show marker only for the first and last waypoints
                                if (i === 0 || i === n-1) {
                                    return L.marker(wp.latLng);
                                }
                            },
                            router: L.Routing.mapbox('pk.eyJ1IjoienNkcmVnYXMiLCJhIjoiY2xicGZnNW9lMDJ1bDNvczM4OTNzcnR2NiJ9.g7US-zEKE8GO5BblQmh9jw',{profile: 'mapbox/walking'}),
                            showAlternatives: false,
                            collapsible: true,
                            show: true,
                            lineOptions:{
                                styles: [{color: 'green', opacity: 1, weigth: 5}]
                            }
                        })
                    }                    
                    this.routingControl.addTo(this.myMap)
                }
        }
    }
    },
    mounted(){
        this.loadMap()
    },
    unmounted(){
        this.myMap = null
    }
};
</script>

<template>
  <div id="mapContainer"></div>
</template>

<style>
#mapContainer {
  height:75vh;
  width: 100%;
  position: relative;
}
.style-good{
    background-color: rgb(80 240 230);
    color: black;
}
.style-fair{
    background-color: rgb(80 204 170);
}
.style-moderate{
    background-color: rgb(240 230 65);
    color: black;
}
.style-poor{
    background-color: rgb(255 80 80);
}
.style-very-poor{
    background-color: rgb(150 0 50);
    color: white;
}
.style-extremely-poor{
    background-color: rgb(125 33 129);
    color: white;
}
</style>