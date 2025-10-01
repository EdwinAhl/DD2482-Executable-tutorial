# Storing secrets locally using OpenBao
## Motivation and Background
Production environments require more attention in the early stages of architecture development and recently many attempts at attacking infrastructure starts at the core. With this in mind, work cannot safely be done unless secure storage of secrets such as API-keys or any similarly sensitive information has been implemented.

## Tutorial Overview
In this tutroial, we will first introduce an insecure example of using plaintext or hardcoded secrets in a Python program. This would show a fast solution, but not a long time secure solution.

Then, we continue with showing how these secrets can be exchanged with a secure solution that controls the storage of secrets, OpenBao. First showing

OpenBao is a fork of HashiCrop Vault that provides the secure storage. Here, OpenBao will be run in a docker container, and commands will be sent to the container in order to communicate with it.

## Intended Learning Outcomes
By the end of this tutorial, you should be able to:
- Setup a password protected database container
- Setup an OpenBao container
- Store and retrieve secrets from the OpenBao container
