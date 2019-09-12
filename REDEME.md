遇到错误：
ERROR [root] Error: cryptography is required for sha256_password or caching_sha2_password
运行三条命令：
处理：

    ALTER USER 'root'@'localhost' IDENTIFIED BY 'password' PASSWORD EXPIRE NEVER; #修改加密规则 
   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password'; #更新一下用户的密码 

   FLUSH PRIVILEGES; #刷新权限 

再重置下密码：alter user 'root'@'localhost' identified by '123qwe';

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

