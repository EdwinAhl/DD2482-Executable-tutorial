# Storing secrets locally using OpenBao
## Motivation and Background
Production environments require more attention in the early stages of architecture development and recently many attempts at attacking infrastructure starts at the core. With this in mind, work cannot safely be done unless secure storage of secrets such as API-keys or any similarly sensitive information has been implemented.

## Tutorial Overview
In this tutroial, we will first introduce an insecure example of using plaintext or hardcoded secrets in a Python program. This would show a fast solution, but not a long time secure solution.

Then, we continue with showing how these secrets can be exchanged with a secure solution that controls the storage of secrets, OpenBao. 

OpenBao is a fork of HashiCrop Vault that provides the secure storage. Here, OpenBao will be run in a docker container, and commands will be sent to the container in order to communicate with it.

```
        Start
          |
+---------v------------+ : Motivation and Background
|        Intro         | : Tutorial Overview
+----------------------+ : ILO
          |
+---------v------------+ : Setup database
| An insecure solution | : Setup Python Virtual environment
+----------------------+ : Connec to DB using plaintext python
          |
+---------v------------+ : Setup OpenBao
|  A secure solution   | : Store Secret in OpenBao
+----------------------+ : Retrieve secret using python http request
          |
+---------v------------+ : Summary
|      Summary         | : Recap
+----------------------+ : Take away
          |
          v
         End
 ```

## Intended Learning Outcomes
By the end of this tutorial, you should be able to:
- Setup a password protected mysql database container
- Understand how OpenBao and tokens works
- Setup your own OpenBao container that uses special policies and tokens to store a secret
- Retrieve a secret from OpenBao using its http api
- Explain one good and one bad practice of storing secrets locally 
