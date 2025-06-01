resource "kubernetes_deployment" "flask_app" {
  metadata {
    name = "flask-app"
    labels = {
      app = "flask-app"
    }
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "flask-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "flask-app"
        }
      }

      spec {
        container {
          image = "flask-app:latest"
          name  = "flask-app"
          image_pull_policy = "Never"
          port {
            container_port = 5000
          }
          resources {
            requests = {
              cpu    = "100m"  # Запрашиваем 100 миллиядер CPU (0.1 ядра)
              memory = "100Mi" # Запрашиваем 100 MiB памяти
            }
            limits = {
              cpu    = "200m"  # Лимит 200 миллиядер CPU (0.2 ядра)
              memory = "200Mi" # Лимит 200 MiB памяти
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_horizontal_pod_autoscaler" "flask_app_hpa" {
  metadata {
    name = "flask-app-hpa"
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = "flask-app"
    }

    min_replicas = 3
    max_replicas = 6
    target_cpu_utilization_percentage = 80
  }
}