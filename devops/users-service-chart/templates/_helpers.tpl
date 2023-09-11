{{/* vim: set filetype=mustache: */}}

{{/*
Expand the name to include the release name and chart name
*/}}
{{- define "users-service-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name "users-service" | trunc 63 | trimSuffix "-" -}}
{{- end }}
