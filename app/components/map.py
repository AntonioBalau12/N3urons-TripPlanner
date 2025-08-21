import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def show_custom_map(location_name):
    """Displays a styled Google Map with contrasting pinpoint"""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        st.error("Google Maps API key not configured")
        return

    # Enhanced map style with better contrast
    map_style = """
    [
        {
            "elementType": "geometry",
            "stylers": [{"color": "#ffffff"}]
        },
        {
            "elementType": "labels.text.fill",
            "stylers": [{"color": "#333333"}]
        },
        {
            "featureType": "water",
            "elementType": "geometry.fill",
            "stylers": [{"color": "#ffb3c6"}]
        },
        {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [{"color": "#ffffff"}]
        },
        {
            "featureType": "road.arterial",
            "elementType": "geometry.stroke",
            "stylers": [{"color": "#fb6f92"}]
        }
    ]
    """

    # HTML/JS with contrasting teal (#00B4D8) marker
    map_html = f"""
    <div style="background-color:#ffb3c6; padding:10px; border-radius:10px; margin-bottom:15px; height:400px;">
        <h4 style="color:#333333; margin-top:0;">{location_name}</h4>
        <div id="map" style="height:350px; width:100%; border-radius:8px;"></div>
    </div>

    <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap" async defer></script>
    <script>
        function initMap() {{
            var map = new google.maps.Map(document.getElementById('map'), {{
                center: {{lat: 0, lng: 0}},
                zoom: 13,
                styles: {map_style},
                zoomControl: true
            }});

            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({{'address': '{location_name}'}}, function(results, status) {{
                if (status === 'OK') {{
                    map.setCenter(results[0].geometry.location);
                    new google.maps.Marker({{
                        map: map,
                        position: results[0].geometry.location,
                        icon: {{
                            path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
                            fillColor: "#00B4D8",  // Teal color
                            fillOpacity: 1,
                            strokeColor: "#ffffff",
                            strokeWeight: 2,
                            scale: 8
                        }},
                        title: '{location_name}'
                    }});
                    map.setZoom(14);
                }} else {{
                    console.error('Geocode failed: ' + status);
                }}
            }});
        }}
    </script>
    """

    st.components.v1.html(map_html, height=450)