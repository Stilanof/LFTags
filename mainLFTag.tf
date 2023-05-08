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


resource "aws_lakeformation_lf_tag" "segclave" {
key = "segclave"
values = [1,2,3]
}
        
resource "aws_lakeformation_lf_tag" "tecensayo" {
key = "tecensayo"
values = [1,2]
}
        