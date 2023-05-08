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

resource "aws_lakeformation_lf_tag" "segAUTO" {
key = "segAUTO"
values = "['ENSAYO']"
}
        
resource "aws_lakeformation_lf_tag" "segnueva" {
key = "segnueva"
values = ['1', '2', '3']
}
        