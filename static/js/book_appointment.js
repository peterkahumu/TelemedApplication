document.addEventListener('DOMContentLoaded', function(){
    /**
     * This function is used to set the value of the doctor_id input field in the requestServicesModal
     * When the user clicks on the "Request Services" button, the doctor_id input field is set to the value of the data-doctor-id attribute of the button
     * This is done so that the doctor_id is sent to the server when the user submits the form to uniquely identify the doctor.
     */
    const requestServicesModal = document.querySelector('#requestServicesModal');
    const doctor_id = document.querySelector("#doctor_id");

    requestServicesModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const id_value = button.getAttribute('data-doctor-id');
        
        doctor_id.value = id_value;
    });
});