# DDoS

## Warning
- If we find any behavior similar to (D)DoS to our service, you may be banned (and thus your homework may be degraded) for several days, depends on the severity.


## Website
- You can see your progress in `https://cnshw3.csie.org`
- Your username is school id with all lower case
- Your password can be found on NTU COOL (assignments → DDoS Password)
- The status will be updated in at most 10 minutes, please be patient

## Server
1. Connect your server via `ssh cns2021@cnshw3.csie.org -i /path/to/id_ed25519_cns`
2. Type in your username (school id with all lower case) and password (you can find it on NTU COOL (assignments → DDoS Password)), then you can start surveying the question
3. Note that the time left for you to input username / password is only 5 seconds, we strongly recommanded you to login using a customized script

## Patch
- You cannot modify anything in `/home/cns/code/` directly
- If you want to patch codes under `/home/cns/code/`, you should connect to `cnshw3.csie.org:9090` (via any tools, e.g. nc, pwntools, etc.)
  - You should input username / password (The same as that of the website and your server)
  - You can only patch one function at a time
  - You should upload your patch after [base64 encoded](https://zh.wikipedia.org/zh-tw/Base64)
  - You should NOT include the function signature. For example, a eligible patch will look like `CWludCBpbnB1dDsKCXNjYW5mKCIlZFxuIiwgJmlucHV0KTsKCXJldHVybiBpbnB1dDsK`
  - Do NOT treat the patch server as a compile server, it is your responsibility to make sure the code is compilable.
  - After input your patch, a test script (which will make sure the necessary function still remains after your patch) will be give, you can test it locally. It will be compiled using `gcc -O0 <test script> -lseccomp`
  - If you received a `success` after your patch, then the patch is successfully uploaded, otherwise, you should try it again
