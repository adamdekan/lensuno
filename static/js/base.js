// checkbox selector
function make_only_one_selected(event) {
var checkbox_list = document.getElementsByName('category');
for (var i = 0; i < checkbox_list.length; i++) {
if (checkbox_list[i].type == 'checkbox' && checkbox_list[i].id !== event.target.id) {
checkbox_list[i].checked = false;
        }
    }
}

// alerts
$(document).ready(function(){
    $('.alert').addClass('alert-fixed').fadeIn().delay(4000).fadeOut();
});

// autocomplete
var onLoaded = function() {
    // I am assuming your field has id of where_load, it might be different
     var location_input = document.getElementById('search');
     var autocomplete = new google.maps.places.Autocomplete(location_input);

 }

// Handle response from server after button click
function copyUrl() {
    var url = window.location.href;
    navigator.clipboard.writeText(url).then(function() {
      document.getElementById('copy-url-share').innerText = 'Link copied!';
    }, function(error) {
      console.error('Failed to copy the URL: ', error);
    });
  }

// gallery gig
