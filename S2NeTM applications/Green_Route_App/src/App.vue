<script>
import LeafletMap from './components/LeafletMap.vue'
import ModalPopup from './components/ModalPopup.vue'
import PointInputs from './components/PointInputs.vue'
import { Entity_AQI, PATH } from './utils/GraphqlQueries.js'

export default {
  components: {
    LeafletMap,
    ModalPopup,
    PointInputs,
   
},
  apollo: {
    Entity_AQI:{
      query: Entity_AQI,
      result ({ data, loading, networkStatus }) {
        this.entities = data.Entity_AQI
      },
      variables() {
        return {
          spList: ["no2", "so2", "o3"],
          partList: ["pm2.5", "pm10"],
          aqiValues: ["Good", "Fair", "Moderate", "Poor", "Very Poor", "Extremely Poor"]
        }
      }
    }
  },
  data() {
    return {
      center:[36.95864, 26.966999],
      isModalOn: false,
      mutationFinished: true,
      startPointLat: 0,
      startPointLng: 0,
      endPointLat: 0,
      endPointLng: 0,
      lat:0,
      lng:0,
      entities: [],
      pointsInPath: [],
      mutationStartPoint: {},
      mutationEndPoint: {}
    }
  },
  mounted(){
    this.$apollo.queries.Entity_AQI.start()

  },
  methods:{
    getRoutePoints({startPoint, endPoint}){
      this.mutationFinished = false
      this.$apollo.mutate({
        mutation: PATH,
        variables: {
            "spList": ["no2","so2","o3"],
            "partList": ["pm2.5","pm10"],
            "aqiValues": ["Good","Fair","Moderate","Poor","Very Poor","Extremely Poor"],
            "properAqi": ["Good","Fair","Moderate","Poor"],
            "startPoint": startPoint ? startPoint:{"latitude": 36.96413219670586, "longitude": 26.952653220606674},
            "endPoint": endPoint?endPoint:{"latitude": 36.95530873325873, "longitude": 26.976775119232496}
          
        }
      }).then((data) => {
          this.mutationFinished = true
          let { Path } = data.data
          let points = []
          const sp = {}
          sp.lat = startPoint.latitude
          sp.long = startPoint.longitude
          points.push(sp)
          for (const point of Path){
            let newPoint = {}
            newPoint.lat = point.lat
            newPoint.long = point.long
            points.push(newPoint)
          }
          const ep = {}
          ep.lat = endPoint.latitude
          ep.long = endPoint.longitude
          points.push(ep)
          this.pointsInPath = points
          console.log(`Points sent:`, points)
        }
      )
    },
    handleChange(event){
      this.isModalOn = true
      this.lat = event.lat
      this.lng = event.lng
    },
    handleModalClosed({startpoint, endpoint}){
      this.isModalOn = false
      if ( startpoint == 'on' ){
        this.startPointLat = this.lat
        this.startPointLng = this.lng
      } else if (endpoint =='off') {
        this.endPointLat = this.lat
        this.endPointLng = this.lng
      }
    }
  }
}
</script>

<template>
  <div class="d-flex justify-content-center align-items-center" style="height: 100vh" v-if="this.$apollo.queries.Entity_AQI.loading">  
      <img src="https://myria.math.aegean.gr/~atsol/newpage/software/aegeanlogo/logo_circle_el_en.png" alt="Logo">
      <div class="spinner-border text-primary" role="status"></div>
  </div>
  

  
    <div class="row" v-else>  
      <div class="col-xs-12 pb-3">
        <PointInputs @setpoints="getRoutePoints" :mutationLoading="!this.mutationFinished" :startPointLat="this.startPointLat" :startPointLng="this.startPointLng" :endPointLat="this.endPointLat" :endPointLng="this.endPointLng" />
      </div>
      <div class="col-xs-12 ">
        <LeafletMap @mapclicked="handleChange" :center="this.center" :data="this.entities" :points="this.pointsInPath" :mutationLoading="!this.mutationFinished"/>
        </div>
  
    </div>
    <div class="col-xs-12 pb-3">
    <footer class="text-center text-white fixed-bottom" style="background-color: #0d6efd;">
      
      <div class="text-center p-2" style="background-color: rgba(0, 0, 0, 0.2);">
        
        © 2023 Copyright: Δημήτρης Λυμπέρης - Πανεπιστήμιο Αιγαίου
      </div>
    
    </footer>
  </div>
    <div v-if="isModalOn">
        <ModalPopup @closed="handleModalClosed" :popupvisible="this.isModalOn"/>
    </div>

</template>


<style scoped>
.logo-container {
  background-color: #ffffff;
  width: 100px;
  height: 100px;
  border-radius: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

img {
  width: 400px;
  height: 400px;
}

.spinner-border {
  position: absolute;
  border-top: 20px solid #ffffff;
  border-right: 20px solid #ffffff;
  border-bottom: 20px solid #ffffff;
  border-left: 20px solid #0069d9;
  width: 500px;
  height: 500px;
  border-radius: 100%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>