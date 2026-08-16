output "api_gateway_url" {
  value = "https://tf-nexus-api-dev.execute-api.${var.region}.amazonaws.com"
}

output "event_bus_arn" {
  value = "arn:aws:events:${var.region}:<account-id>:event-bus/telcoflow-nexus-events"
}
