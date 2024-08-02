variable "api_name" {
  type = string
}

variable "env" {
  type = string
}

# TODO/contibution: modularize and add domain name.
variable "domain_name" {
  type    = string
  default = ""
}

variable "app_function_name" {
  type = string
}

variable "auth_function_name" {
  type = string
}

variable "ecr_repo_name" {
  type = string
}

variable "image_tag" {
  type = string
}