'use strict';

// Create a map variable
var map;
// Create a new blank array for all the listing markers.
var markers = [];

// Initialize the map
function initMap() {
  // TODO: use a constructor to create a new map JS object. 
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat:37, lng:-121},
    zoom:9
  });

  var ul = document.getElementById('marker_list');
  
  var largeInfowindow = new google.maps.InfoWindow();

  var locations = [  
    {title: 'My Delicious Tiramisu', location: {lat: 37.3513641357422, lng: -121.952194213867}, id: 'my-delicious-tiramisu-santa-clara-16' },
    {title: 'Stan\'s Donut Shop', location: {lat: 37.338861954274, lng: -121.97310467526}, id: 'stans-donut-shop-santa-clara' },
    {title: 'Fairycakes', location: {lat: 37.3589414, lng: -121.9392165}, id: 'fairycakes-santa-clara' },
    {title: 'Barbara of Pauline\'s Cake Decorating Supplies', location: {lat: 37.2938804626465, lng: -121.889755249023}, id: 'barbara-of-paulines-cake-decorating-supplies-san-jose' },
    {title: 'Not Just Cheesecakes', location: {lat: 37.287356616022, lng: -121.938364793848}, id: 'not-just-cheesecakes-campbell' },
    {title: 'Nothing Bundt Cakes', location: {lat: 37.3718548618985, lng: -122.046209806747}, id: 'nothing-bundt-cakes-sunnyvale' },
    {title: 'Hannah', location: {lat: 37.331594567997, lng: -121.905520934925}, id: 'hannah-san-jose' },
    {title: 'The Cake Man', location: {lat: 37.3100814819336, lng: -121.962646484375}, id: 'the-cake-man-san-jose-2' },
    {title: 'Sweets By Design', location: {lat: 37.3161735534668, lng: -121.936302185059}, id: 'sweets-by-design-san-jose-4' },
    {title: 'Cake Expressions', location: {lat: 37.3637809753418, lng: -121.94091796875}, id: 'cake-expressions-santa-clara' },
    {title: 'Mission City Creamery', location: {lat: 37.3456058, lng: -121.9375109}, id: 'mission-city-creamery-santa-clara' },
    {title: 'Jen\'s Cakes', location: {lat: 37.3106, lng: -121.90302}, id: 'jens-cakes-san-jose' },
    {title: 'Linda\'s Bakery', location: {lat: 37.3442999, lng: -121.87282}, id: 'lindas-bakery-san-jose' },
    {title: 'Haleh Pastry', location: {lat: 37.28211, lng: -121.95016}, id: 'haleh-pastry-campbell' },
    {title: 'Bill\'s Café', location: {lat: 37.34303, lng: -121.92846}, id: 'bills-café-san-jose-9' },
    {title: 'Sweet Tooth Confections', location: {lat: 37.33748, lng: -121.93846}, id: 'sweet-tooth-confections-san-jose' },
    {title: 'Bitter+Sweet', location: {lat: 37.3181638185566, lng: -122.03151641898}, id: 'bitter-sweet-cupertino' } 
  ];

  var defaultIcon = makeMarkerIcon('0091ff');
  // Create a "highlighted location" marker color for when the user
  // mouses over the marker.
  var highlightedIcon = makeMarkerIcon('FFFF24');

  // The following group uses the location array to create an array of markers on initialize.
  for (var i = 0; i < locations.length; i++) {
    var pin;
    pin = new Pin(map, locations[i].title, locations[i].location, locations[i].id);

    // Push the marker to our array of markers.
    markers.push(pin);

    // Create an onclick event to open the large infowindow at each marker.
    pin.marker.addListener('click', function() {
      var marker = this;
      if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
      } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
      };
      populateInfoWindow(marker, largeInfowindow);
    });

    // Two event listeners - one for mouseover, one for mouseout,
    // to change the colors back and forth.
    pin.marker.addListener('mouseover', function() {
      this.setIcon(highlightedIcon);
    });
    pin.marker.addListener('mouseout', function() {
      this.setIcon(defaultIcon);
    });

  } // end of for-loop

  // Extend the boundaries of the map for each marker and display the marker
  var bounds = new google.maps.LatLngBounds();
  for (var i = 0; i < markers.length; i++) {
    markers[i].marker.setMap(map);
    bounds.extend(markers[i].marker.position);
  }
  map.fitBounds(bounds);

  // finally set map and markers into viewmodel
  ko.applyBindings(new ViewModel(map, markers));

} // end of initMap

// Wrap isVisible flag with marker for filtering
function Pin(map, name, position, id) {
  var self = this;

  // Get the position from the location array.
  self.position = position;
  self.name = ko.observable(name);
  self.id = id;
  // Create a marker per location, and put into markers array.
  var defaultIcon = makeMarkerIcon('0091ff');
  var marker = new google.maps.Marker({
    position: position,
    title: name,
    animation: google.maps.Animation.DROP,
    icon: defaultIcon,
    yelp_id: id
  });
  self.marker = marker;
  
  self.isVisible = ko.observable();
  self.isVisible.subscribe(function(currentState) {
    if (currentState) {
      marker.setMap(map);
    } else {
      marker.setMap(null);
    }
  });

  self.isVisible(true);
}

// This function takes in a COLOR, and then creates a new marker
// icon of that color. The icon will be 21 px wide by 34 high, have an origin
// of 0, 0 and be anchored at 10, 34).
function makeMarkerIcon(markerColor) {
  var markerImage = new google.maps.MarkerImage(
    'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
    '|40|_|%E2%80%A2',
    new google.maps.Size(21, 34),
    new google.maps.Point(0, 0),
    new google.maps.Point(10, 34),
    new google.maps.Size(21,34));
  return markerImage;
}

// This function populates the infowindow when the marker is clicked. We'll only allow
// one infowindow which will open at the marker that is clicked, and populate based
// on that markers position.
function populateInfoWindow(marker, infowindow) {
  // Check to make sure the infowindow is not already opened on this marker.
  if (infowindow.marker != marker) {
    // Clear the infowindow content to give the streetview time to load.
    infowindow.setContent('');
    infowindow.marker = marker;
    // Make sure the marker property is cleared if the infowindow is closed.
    infowindow.addListener('closeclick', function() {
      infowindow.marker = null;
    });

    // Set Yelp info
    yelpInfo(marker.yelp_id, function(data) {
        var content = "<div class = 'MarkerPopUp' id='iw-container'>" +
                      "<div class='iw-title'><a href='" + data.url + "'>" + data.name + "</a></div>" +
                      '<div class="iw-content">' +
                       '<div class="iw-subTitle">Yelp Review</div>' +
                       "<img src='" + data.image_url + "' height='115' width='83'></img>" +
                       "<p>" + data.snippet_text + "</p>" +
                       '<div class="iw-subTitle">Contacts</div>' +
                       "<p>" + data.location.address + "</p>" +
                       "<p>" + data.display_phone + "</p>" +
                      "</div>";
        infowindow.setContent(content);
    });

    // Open the infowindow on the correct marker.
    infowindow.open(map, marker);
  }
}

function ViewModel(map, markers) {
  var self = this;
  self.pins  = ko.observableArray(markers);
  self.clickHandler = function(pin) {
    google.maps.event.trigger(pin.marker, "click");
  }

  self.query = ko.observable('');
  self.filterPins = ko.computed(function () {
      var search  = self.query().toLowerCase();

      console.log(self.pins().length);
      return ko.utils.arrayFilter(self.pins(), function (pin) { 
          var doesMatch = pin.name().toLowerCase().indexOf(search) >= 0;
          pin.isVisible(doesMatch);

          return doesMatch;
      });
  });
}