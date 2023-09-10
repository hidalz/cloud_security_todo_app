{{/* Set the name for this chart */}}
{{- define "auth-service-chart.fullname" -}}
{{- printf "%s-auth-service" .Release.Name }}
{{- end }}
