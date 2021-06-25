# HALO


## What it does

- Primary visualization portal for the HALO project
- Built as Docker Stack with four containers:
  1. web portal (Python/Flask/mod_wsgi)
  2. tools (Ubuntu container)
  3. local db (MongoDB)
  4. ERDDAP server
- Retrieves data streams from multiple instruments and sources
- Creates compliant NetCDF files from data and stores in ERDDAP server
- Creates visualization layers for Leaflet map
- Provides multiple overlays
- Pulls data from DBHYDRO and converts to GeoJSON feature collection
- Uses GANDALF tools to monitor Navocean ASV
- Rules the universe


## Feedback

This is a work in progress and will change on a daily basis

## License

Copyright 2019 GCOOS-RA, Inc.

Licensed to the Apache Software Foundation (ASF) under one or more contributor
license agreements. See the NOTICE file distributed with this work for
additional information regarding copyright ownership. The ASF licenses this
file to you under the Apache License, Version 2.0 (the “License”); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
