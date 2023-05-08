terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}
provider "aws" {
  region                   = "us-east-1"
}


      
resource "aws_lakeformation_lf_tag" "tecAUTO" {
key = "tecAUTO"
values = [1,2]
}
        