// JavaScript to handle profile picture upload preview
document.getElementById('profile-picture-upload').addEventListener('change', function(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const output = document.getElementById('profile-picture');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
});