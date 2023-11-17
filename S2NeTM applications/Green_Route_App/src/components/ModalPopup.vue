<script>
import { Modal } from "bootstrap";

  export default{
    name: 'ModalPopup',
    props: ['popupvisible'],
    data(){
      return {
        thisModalObj: null,
        visible: false,
        pointA: null,
        pointB: null
      }
    },
    methods:{
      closePopUp(){
        this.thisModalObj.hide()
        this.$emit('closed', {startpoint: this.pointA, endpoint: this.pointB})
      },
      togglePopup(){
        if (!this.thisModalObj){
          this.thisModalObj = new Modal(document.getElementById('staticBackdrop'), {});
        }
        if (this.popupvisible){
          this.thisModalObj.show()
        }
      }
    },
    mounted(){
      this.togglePopup()
    }
  }
</script>
<template>
  <div class="modal fade" id="staticBackdrop"  data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-sm">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">Επιλογή Σημείου</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Κλείσιμο"></button>
        </div>
        <div class="modal-body">
          <div class="form-check  form-check-inline">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" v-model="pointA" value='on'/>
            <label class="form-check-label" for="flexRadioDefault1">Αρχικό</label>
          </div>
          <div class="form-check  form-check-inline">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" v-model="pointB" value='off'/>
            <label class="form-check-label" for="flexRadioDefault2">Τελικό</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closePopUp">Κλείσιμο</button>
        </div>
      </div>
    </div>
  </div>
</template>