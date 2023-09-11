{{/* templates/_helpers.tpl */}}

{{- define "api-gateway-chart.fullname" -}}
{{- printf "%s-api-gateway-service" .Release.Name -}}
{{- end -}}
