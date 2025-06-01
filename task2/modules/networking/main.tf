resource "kubernetes_service" "flask_app_service" {
  metadata {
    name = "flask-app-service"
  }

  spec {
    selector = {
      app = "flask-app"
    }

    port {
      port        = 80
      target_port = 5000
    }

    type = "LoadBalancer"
  }
}