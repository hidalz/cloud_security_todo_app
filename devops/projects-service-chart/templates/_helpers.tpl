{{- define "projects-service-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name "projects-service" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
