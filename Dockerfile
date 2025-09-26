# Use an official Gatus image as the base
FROM twinn/gatus:stable

# Gatus looks for its configuration in the /config directory by default
# We will copy our final, aggregated config file here during the build process
COPY ./config.yaml /config/config.yaml