# Windows setup guide
You only need to setup once on your PC. Once you have finished the setup process, you just need to run `main.exe` everytime you want to fill the survey.

## Get a Duo activation link

Log in to a Duo authentication page, click  `Add a new device`.

![](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/32e0cc06-1e92-4cc4-8ac1-522595989727/Screen_Shot_2022-04-12_at_7.19.26_AM.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220412%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220412T141937Z&X-Amz-Expires=86400&X-Amz-Signature=93448629bb7a0f673df36bb6160a4575b7c1ed4cef3a6c58f5ad086dd89a622e&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Screen%2520Shot%25202022-04-12%2520at%25207.19.26%2520AM.png%22&x-id=GetObject)

After verified, choose  `Tablet`, choose either  `iOS`  or  `Android`, and click  `Continue`. 

Click  `I have Duo Mobile installed`, and click  `Email me an activation link instead`. 

Enter your email and click `Send email`.

![](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/f965ce1f-f081-4565-9a71-6deff3d40355/Screen_Shot_2022-04-12_at_7.22.24_AM.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220412%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220412T142231Z&X-Amz-Expires=86400&X-Amz-Signature=10259f768c5cd2902cc92d3762facda63b92f34fa8a52ddefa2d7e521b0b3c6a&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Screen%2520Shot%25202022-04-12%2520at%25207.22.24%2520AM.png%22&x-id=GetObject)

You'll receive an email called `Duo Mobile Activation` soon. Copy the activation link in the email.

![](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/bb75c03f-78fe-4d54-8135-74d7c21590f4/Screen_Shot_2022-04-12_at_7.24.31_AM.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220412%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220412T142519Z&X-Amz-Expires=86400&X-Amz-Signature=9caa26f99dd94cdeed0c7105ea6076d24956d15a32902bcd98c2297e16cbb11d&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Screen%2520Shot%25202022-04-12%2520at%25207.24.31%2520AM.png%22&x-id=GetObject)

## Run the auto-filling script
Double Click and run `main.exe`, and you will be greated with a command line interface. Paste the link you just obtained.

![alt text](https://github.com/MubaiHua/ucla-cat/blob/main/images/win_exe.png?raw=true)

Enter your UCLA Logon ID and password. Then a chrome window will pop up and the survey will start auto-filling.

You only need to enter the activation link or account information for this first time. From now on, you can run `main.exe` and the survey will be auto-filled on its own.