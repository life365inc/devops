import sys
import json
import paramiko
from io import StringIO
from fabric import Connection
import codecs

if __name__ == "__main__":
  key_index = f"{sys.argv[3]}_ssh_key"
  ip_index = f"{sys.argv[3]}_IP"
  secret_obj = {}
  secret_str = sys.argv[2][1:]
  secret_str = secret_str[:-1]
  secret_arr = secret_str.split(",")
  for section in secret_arr:
    temp_arr = section.split(":")
    secret_obj[temp_arr[0]] = temp_arr[1]
  raw_key = codecs.decode(secret_obj[key_index][:-2], 'unicode_escape')
  print(raw_key)
  # Builds RSA key to be used in SSH
  my_key = f"-----BEGIN RSA PRIVATE KEY-----\n{raw_key}\n-----END RSA PRIVATE KEY-----"
  print(my_key)
  pkey = paramiko.RSAKey.from_private_key(StringIO(my_key))
  def pull(pkey, ip, image, tag):
    conn = Connection(
        host=f'{ip}',
        user="ubuntu",
        connect_kwargs={
            "pkey": pkey,
        },
    )
    try:
        print(f"......pulling docker image {image}......")
        conn.run(f"docker pull life365inc/{image}:{tag}")
        conn.close()
    except:
        raise ValueError("Unable to execute")


  def deploy(pkey, ip, image):
    conn = Connection(
        host=f'{ip}',
        user="ubuntu",
        connect_kwargs={
            "pkey": pkey,
        },
    )
    try:
        exe_cmd = "~/l365/l365 start"
        if sys.argv[3] == "staging1":
          exe_cmd = "docker-compose -f ssl-compose.yml up -d"
        print(f"......deploying {image}......")
        conn.run(exe_cmd)
        conn.close()
    except:
        raise ValueError("Unable to execute")


  if sys.argv[1] == "pull":
    pull(pkey, secret_obj[ip_index], sys.argv[4], sys.argv[5])
  else:
    deploy(pkey, secret_obj[ip_index], sys.argv[4])
    
