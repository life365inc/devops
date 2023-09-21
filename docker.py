import sys
import json
import paramiko
from io import StringIO

if __name__ == "__main__":
  secret_obj = {}
  secret_str = sys.argv[2][1:]
  secret_str = secret_str[:-1]
  secret_arr = secret_str.split(",")
  for section in secret_arr:
    temp_arr = section.split(":")
    secret_obj[temp_arr[0]] = temp_arr[1]
  # Builds RSA key to be used in SSH
  my_key = f"""-----BEGIN RSA PRIVATE KEY-----
  {secret_obj.staging1_ssh_key}
  -----END RSA PRIVATE KEY-----"""
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
        print(f"......deploying {image}......")
        conn.run(f"~/l365/l365 start")
        conn.close()
    except:
        raise ValueError("Unable to execute")


  if sys.argv[1] == "pull":
    pull(pkey, secret_obj.staging1_IP, sys.argv[4], sys.argv[5])
  else:
    deploy(pkey, secret_obj.staging1_IP, sys.argv[4])
    
