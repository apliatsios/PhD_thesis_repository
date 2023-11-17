<script>
  export default {
    name: 'PointInputs',
    emits:['setpoints'],
    props:[
      'startPointLat',
      'startPointLng',
      'endPointLat',
      'endPointLng',
      'mutationLoading'
    ],
    data() {
      return {
        startLat:0,
        startLng:0,
        endLat:0,
        endLng:0
      }
    },
    methods:{
      getDistance(origin, destination) {
        // return distance in meters
        const lon1 = this.toRadian(origin[1]),
              lat1 = this.toRadian(origin[0]),
              lon2 = this.toRadian(destination[1]),
              lat2 = this.toRadian(destination[0]);

        const deltaLat = lat2 - lat1;
        const deltaLon = lon2 - lon1;

        const a = Math.pow(Math.sin(deltaLat/2), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(deltaLon/2), 2);
        const c = 2 * Math.asin(Math.sqrt(a));
        const EARTH_RADIUS = 6371;
        return c * EARTH_RADIUS * 1000;
    },
    toRadian(degree) {
        return degree*Math.PI/180;
    },
      setInitialValues(){
        this.startLat = this.startPointLat
        this.startLng = this.startPointLng
        this.endLat = this.endPointLat
        this.endLng = this.endPointLng
      },
      getPoints(){
        const spLat = parseFloat(localStorage.getItem('spLat'))
        const spLng = parseFloat(localStorage.getItem('spLng'))
        const epLat = parseFloat(localStorage.getItem('epLat'))
        const epLng = parseFloat(localStorage.getItem('epLng'))
        if (spLat!=this.startLat || spLng!=this.startLng || epLat!=this.endLat || epLng!=this.endLng) {
          this.$emit('setpoints', {startPoint:{latitude:this.startLat, longitude:this.startLng}, endPoint:{latitude:this.endLat, longitude:this.endLng}})
          localStorage.setItem('spLat', this.startLat.toString())
          localStorage.setItem('spLng', this.startLng.toString())
          localStorage.setItem('epLat',  this.endLat.toString())
          localStorage.setItem('epLng',  this.endLng.toString())
        }
      }
    },
    computed:{
      pointValuesValid(){
        // return this.startLat>0 && this.startLng>0 & this.endLat>0 & this.endLng>0
        return this.getDistance([this.startLat, this.startLng], [this.endLat, this.endLng]) > 100
      }
    },
    mounted(){
      this.setInitialValues()
    },
    beforeUpdate(){
      this.setInitialValues()
    }
  }
</script>

<template>
  <!-- <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
    Button with data-target
  </button> -->
  <!-- <div class="collapse" id="collapseExample"> -->
    
    <div class="row">
      <label for="StartPointLat" class="col-sm-2 col-form-label"><h5>Αρχικό Σημείο:</h5></label>
      <div class="col-sm-5">
        <div class="input-group">
          <div class="input-group-text" id="startLat">Lat</div>
          <input type="text" id="StartPointLat" class="form-control" placeholder="ΓΠ Αρχικού Σημείου" aria-label="StartPointLat" aria-describedby="startLat" v-model="this.startLat">
        </div>
      </div>
      <div class="col-sm-5">
        <div class="input-group">
          <div class="input-group-text" id="startLng1">Lng</div>
          <input type="text" class="form-control"  aria-label="StartPointLng" aria-describedby="startLng1" v-model="this.startLng">
      </div>
    </div>
    </div>
  
      <div class="row mb-3">
        <label for="endpointlat" class="col-sm-2 col-form-label"><h5>Τελικό σημείο:</h5></label>
         <div class="col-sm-5">
          <div class="input-group" >
            <span class="input-group-text" id="endLat1">Lat</span>
            <input type="text" class="form-control" id="endpointlat" aria-label="EndPointLat" aria-describedby="endLat1" v-model="this.endLat">
          </div>
        </div>
        <div class="col-sm-5">
          <div class="input-group">

            <span class="input-group-text" id="endLng1">Lng</span>
            <input type="text" class="form-control col-sm"  aria-label="EndPointLng" aria-describedby="endLng1" v-model="this.endLng">
          </div>
        </div>
      </div>

    <!-- s</div> -->
    <div class="row">
      <div class="d-grid gap-2">
         <button class="btn btn-primary" type="button" :disabled="!this.pointValuesValid" @click="getPoints">
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" v-if="this.mutationLoading"></span>
          <span class="visually-hidden">Loading...</span>
          
          Υπολογισμός Διαδρομής
        </button>
      </div>
      
    </div>

</template>
<style>


</style>