provider "kubernetes" {
  config_path = "~/.kube/config"
}

module "compute" {
  source = "./modules/compute"
}

module "networking" {
  source = "./modules/networking"
}