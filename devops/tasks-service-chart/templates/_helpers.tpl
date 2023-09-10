{{/* vim: set filetype=mustache: */}}

{{/*
Expand the name to include the release name and chart name
*/}}
{{- define "tasks-service-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name "tasks-service" | trunc 63 | trimSuffix "-" -}}
{{- end }}
