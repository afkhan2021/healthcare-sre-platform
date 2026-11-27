module "ecr" {
  source = "../../modules/ecr"

  project_name     = var.project_name
  environment      = var.environment
  repository_names = var.repository_names
}

module "github_oidc" {
  source = "../../modules/github-oidc"

  project_name        = var.project_name
  environment         = var.environment
  github_repository   = var.github_repository
  github_branch       = var.github_branch
  ecr_repository_arns = values(module.ecr.repository_arns)
}
