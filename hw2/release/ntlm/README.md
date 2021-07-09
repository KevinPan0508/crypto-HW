# NTLMv2 Authentication
-----------------------

- This challenge require you to communicate with a NTLMv2 authentication server
- There are mainly two function
  - register: register a account with a password
  - login: login through the NTLMv2 procedure, you can refer to the [specification](https://curl.se/rfc/ntlm.html) for your implementation. Note that except for the error message, the authentication procedure follows the specification, e.g. you will have to send message with type 1 first if you want to login.
