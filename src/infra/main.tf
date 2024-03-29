terraform {
  required_providers {
    google = {
      source  = "hashicorp/google-beta"
      version = "4.25.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Enable IAM API
#resource "google_project_service" "iam" {
#  provider = google
#  service            = "iam.googleapis.com"
#  disable_on_destroy = false
#}
#
## Enable Artifact Registry API
#resource "google_project_service" "artifactregistry" {
#  provider = google
#  service            = "artifactregistry.googleapis.com"
#  disable_on_destroy = false
#}
#
##############################################
##               Enable API's                #
##############################################
#
## Enable Cloud Run API
#resource "google_project_service" "cloudrun" {
#  provider = google
#  service            = "run.googleapis.com"
#  disable_on_destroy = false
#}
#
## Enable Cloud Resource Manager API
#resource "google_project_service" "resourcemanager" {
#  provider = google
#  service            = "cloudresourcemanager.googleapis.com"
#  disable_on_destroy = false
#}
#
#resource "time_sleep" "wait_30_seconds" {
#  create_duration = "30s"
#  depends_on = [
#    google_project_service.iam,
#    google_project_service.artifactregistry,
#    google_project_service.cloudrun,
#    google_project_service.resourcemanager
#    ]
#}
#
##############################################
##    Google Artifact Registry Repository    #
##############################################
#
## Create Artifact Registry Repository for Docker containers
#resource "google_artifact_registry_repository" "my_docker_repo" {
#  provider = google
#
#  location = var.region
#  repository_id = var.repository
#  description = "My docker repository"
#  format = "DOCKER"
#  depends_on = [time_sleep.wait_30_seconds]
#}
#
## Create a service account
#resource "google_service_account" "docker_pusher" {
#  provider = google
#
#  account_id   = "docker-pusher"
#  display_name = "Docker Container Pusher"
#  depends_on =[time_sleep.wait_30_seconds]
#}
#
## Give service account permission to push to the Artifact Registry Repository
#resource "google_artifact_registry_repository_iam_member" "docker_pusher_iam" {
#  provider = google
#
#  location = google_artifact_registry_repository.my_docker_repo.location
#  repository =  google_artifact_registry_repository.my_docker_repo.repository_id
#  role   = "roles/artifactregistry.writer"
#  member = "serviceAccount:${google_service_account.docker_pusher.email}"
#  depends_on = [
#    google_artifact_registry_repository.my_docker_repo,
#    google_service_account.docker_pusher
#    ]
#}


##############################################
#       Deploy API to Google Cloud Run       #
##############################################

# Deploy image to Cloud Run
resource "google_cloud_run_service" "api_test" {
  provider = google
  name     = "chat-agh"
  location = var.region
  template {
    spec {
        containers {
            image = "europe-west4-docker.pkg.dev/${var.project_id}/${var.repository}/${var.docker_image}"
            resources {
                limits = {
                "memory" = "1G"
                "cpu" = "1"
                }
            }
        }
    }
    metadata {
        annotations = {
            "autoscaling.knative.dev/minScale" = "0"
            "autoscaling.knative.dev/maxScale" = "1"
        }
    }
  }
  traffic {
    percent = 100
    latest_revision = true
  }
#  depends_on = [google_artifact_registry_repository_iam_member.docker_pusher_iam]
}

# Create a policy that allows all users to invoke the API
data "google_iam_policy" "noauth" {
  provider = google
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# Apply the no-authentication policy to our Cloud Run Service.
resource "google_cloud_run_service_iam_policy" "noauth" {
  provider = google
  location    = var.region
  project     = var.project_id
  service     = google_cloud_run_service.api_test.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

output "cloud_run_instance_url" {
  value = google_cloud_run_service.api_test.status.0.url
}