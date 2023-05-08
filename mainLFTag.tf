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

 
resource "aws_lakeformation_lf_tag" "tecjn" {
key = "tecjn"
values = ["kp"]
}
        
resource "aws_lakeformation_lf_tag" "tecnuevo" {
key = "tecnuevo"
values = {'1'}
}
        
resource "aws_lakeformation_lf_tag" "tecnuevos" {
key = "tecnuevos"
values = {'s', 'd'}
}
        
resource "aws_lakeformation_lf_tag" "segj" {
key = "segj"
values = {'m'}
}
        