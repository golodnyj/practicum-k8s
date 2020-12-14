apiVersion: apps/v1
kind: Deployment
metadata:
  name: lab-demo
  labels:
    app-label: lab-demo-label
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app-label: lab-demo-label
  template:
    metadata:
      labels:
        app-label: lab-demo-label
    spec:
      containers:
      - name: lab-demo-app
        image: cr.yandex/$REGISTRY_ID/lab-demo:v1
        env:
        - name: DATABASE_URI
          value: "$DATABASE_URI"
        - name: DATABASE_HOSTS
          value: "$DATABASE_HOSTS"
