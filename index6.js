// ... (Your existing variable declarations and data fetching code) ...

// Assuming your dropdown has an id of 'iso3-dropdown'
const dropdown = document.getElementById('iso3-dropdown');

// Event listener for dropdown changes
dropdown.addEventListener('change', function() {
  const selectedISO3 = dropdown.value;

  // Filter the map based on the selected ISO3
  if (selectedISO3) {
    map.setFilter('countries-fill', ['==', ['get', 'iso_a3'], selectedISO3]); // Assuming 'iso_a3' is your GeoJSON property
  } else {
    map.setFilter('countries-fill', null); // Show all countries
  }
});

// Initialize the map after data is fetched
function initMap() {
  mapboxgl.accessToken = mapboxAccessToken;

  map = new mapboxgl.Map({
    container: 'myDiv',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [0, 0],
    zoom: 1.5
  });

  // ... (Your existing map initialization code) ...

  // Click event handler for the map
  map.on('click', 'countries-fill', function (e) {
    const clickedFeature = e.features[0];
    const countryISO = clickedFeature.properties.iso_a3; // Assuming 'iso_a3' is your GeoJSON property

    // Find the matching row in your Domo data
    const row = countryData.find(item => item.countryISO3 === countryISO);

    if (row) {
      try {
        // Parse the JSON string
        const jsonData = JSON.parse(row.value);

        // Access the properties from the parsed JSON
        const population = jsonData.Population;
        const landArea = jsonData['Land Area']; // Access with bracket notation due to space

        // Create the popup content
        const popupContent = `
          <table>
            <tr><td>Population:</td><td>${population}</td></tr>
            <tr><td>Land Area:</td><td>${landArea}</td></tr>
          </table>
        `;

        // Display the popup
        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(popupContent)
          .addTo(map);

      } catch (error) {
        console.error('Error parsing JSON:', error);
        console.log('JSON String:', row.value);
        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setHTML('Error parsing data.')
          .addTo(map);
      }
    } else {
      console.warn('No data found for ISO:', countryISO);
    }
  });

  // ... (Your existing map layer additions) ...
}

// Fetch data from Domo and initialize the map
domo.get(query).then(function(data) {
  console.log('Raw dataset from Domo:', data);
  countryData = data; // Store the data in a variable

  initMap(); // Initialize the map after data is fetched
});