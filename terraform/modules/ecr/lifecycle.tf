resource "aws_ecr_lifecycle_policy" "this" {
  for_each = aws_ecr_repository.this

  repository = each.value.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Retain only the 2 most recently pushed tagged images"

        selection = {
          tagStatus   = "tagged"
          countType   = "imageCountMoreThan"
          countNumber = 2
        }

        action = {
          type = "expire"
        }
      }
    ]
  })
}
