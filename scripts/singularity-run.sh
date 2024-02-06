#!/bin/bash

singularity exec image_cutouts_soda_singularity.sif cutouts_soda --survey-dir ./Survey_Images --output-dir ./cutouts Sources.lis
