document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.display = 'none';
        });
    }, 5000);
  });

document.querySelectorAll('label.required').forEach(label => {
    label.innerHTML += '<span style="color: red;">*</span>';
});