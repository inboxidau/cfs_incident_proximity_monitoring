import requests
from geopy.distance import geodesic  # type: ignore
import paho.mqtt.client as mqtt # type: ignore

#pip install geopy
#pip install paho-mqtt

message =  str(0) # default alert detection message is 0 meaning alert off

def fetch_incident_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.json()

def calculate_distance(coord1, coord2):
    """Calculate the distance between two geographic coordinates."""
    return geodesic(coord1, coord2).kilometers

def filter_incidents_within_range(incidents, target_locations_and_thresholds):
    """
    Filter incidents within range of any target location based on specific distance thresholds.

    Parameters:
        incidents (list): List of incident data.
        target_locations_and_thresholds (list of tuples): Each tuple contains a target name, location, and distance threshold.

    Returns:
        list: Filtered incidents within the specified ranges.
    """
    global message
    filtered_incidents = []
    for incident in incidents:
        if (incident["Status"] != "COMPLETE") and (incident["Level"] != 1):
            incident_location = tuple(map(float, incident["Location"].split(',')))
            for name, target_location, distance_threshold in target_locations_and_thresholds:
                if calculate_distance(target_location, incident_location) <= distance_threshold:
                    filtered_incidents.append(incident)
                    message = str(1)
                    break  # Stop checking other target locations for this incident
    return filtered_incidents

def print_incidents(incidents, target_locations_and_thresholds):
    """
    Print details of incidents with the distance from the nearest target location and the threshold used.

    Parameters:
        incidents (list): List of filtered incidents.
        target_locations_and_thresholds (list of tuples): Each tuple contains a target name, location, and distance threshold.
    """
    for incident in incidents:
        incident_location = tuple(map(float, incident["Location"].split(',')))
        # Find the nearest target location's distance
        distance_from_nearest_target = min(
            calculate_distance(target_location, incident_location)
            for _, target_location, _ in target_locations_and_thresholds
        )
        # Determine which distance threshold was used
        threshold_used = next(
            distance_threshold
            for _, target_location, distance_threshold in target_locations_and_thresholds
            if calculate_distance(target_location, incident_location) <= distance_threshold
        )
        # Determine the name of the target location used
        target_name = next(
            name
            for name, target_location, distance_threshold in target_locations_and_thresholds
            if calculate_distance(target_location, incident_location) <= distance_threshold
        )
        # Print the incident details
        print(f"IncidentNo: {incident['IncidentNo']}")
        print(f"Level: {incident['Level']}")
        print(f"Location: {incident['Location_name']}")
        print(f"Type: {incident['Type']}")
        print(f"Status: {incident['Status']}")
        print(f"Distance from nearest target location: {distance_from_nearest_target:.2f} km")
        print(f"Distance threshold used: {threshold_used} km")
        print(f"Target location used: {target_name}")
        print()

def publish_mqtt_message(message, broker_url, broker_port, username, password, topic, cafile, keyfile, certfile):
    """Publish a message to an MQTT broker."""

    # Create MQTT client
    client = mqtt.Client()
    
    # Set TLS configuration
    client.tls_set(ca_certs=cafile)
    client.tls_insecure_set(True)

    # Set username and password
    client.username_pw_set(username, password)

    # Connect to MQTT broker
    client.connect(broker_url, broker_port)

    # Publish message
    client.publish(topic, message)

    # Disconnect from MQTT broker
    client.disconnect()  


def main():

    global message

    url = "https://data.eso.sa.gov.au/prod/cfs/criimson/cfs_current_incidents.json"
    target_locations_and_thresholds = [
        ("Elizabeth South", (-34.73182000, 138.66192000), 10)  # Target location with a distance threshold of 10 km
        ,("Goolwa", (-35.50474000, 138.77320000), 5)   # Another target location with a distance threshold of 5 km
        ,("Adelaide", (-34.92850000, 138.60074000), 50)   # Another target location with a distance threshold of 5 km
    ]

    # Fetch CFS incident data
    cfs_incidents = fetch_incident_data(url)
    
    # Filter incidents
    filtered_incidents = filter_incidents_within_range(cfs_incidents, target_locations_and_thresholds)
    
    # Print filtered incidents
    print_incidents(filtered_incidents, target_locations_and_thresholds)

    # MQTT Broker Settings
    broker_url = "mqttpserver.local"
    broker_port = 8883
    username = "mqttusername"
    password = "mqttpassword"
    topic = "CFSAlert/incidentdetectedTESTING"

    # TLS Configuration
    cafile = "./ca.crt"
    keyfile = ""
    certfile = ""

    # Publish MQTT message
    publish_mqtt_message(message, broker_url, broker_port, username, password, topic, cafile, keyfile, certfile)


if __name__ == "__main__":
    main()
