[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=inboxidau_cfs_incident_proximity_monitoring)](https://sonarcloud.io/summary/new_code?id=inboxidau_cfs_incident_proximity_monitoring)
[![flake8 lint](https://github.com/inboxidau/cfs_incident_proximity_monitoring/actions/workflows/flake8.yml/badge.svg)](https://github.com/inboxidau/cfs_incident_proximity_monitoring/actions/workflows/flake8.yml)
[![CodeQL](https://github.com/inboxidau/cfs_incident_proximity_monitoring/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/inboxidau/cfs_incident_proximity_monitoring/actions/workflows/github-code-scanning/codeql)

# cfs_incident_proximity_monitoring

**cfs_incident_proximity_monitoring** retrieves incident status information from the South Australian Country Fire Service and sends alerts to an MQTT queue.

## Features

- Monitors incidents not marked as COMPLETE.
- Alerts for incidents with a threat level indicating "watch and act."
- Sends alerts to an MQTT queue integrated with a Homebridge leak detector for Apple HomeKit notifications.

## Configuration

1. Provide a list of GPS coordinates for points of interest.
2. Specify the name and radius for each point of interest.

## Integration

The alerts are configured to work with a Homebridge leak detector, allowing you to receive notifications on your Apple HomeKit ecosystem. 

- [Homebridge](https://homebridge.io/)
- [South Australian Country Fire Service (CFS)](https://www.cfs.sa.gov.au/warnings-restrictions/warnings/incidents-warnings/)
