import requests
from requests.auth import HTTPBasicAuth
from encryption import RSA, Encryption
import random

while True:
    print("")
    print("-login: \tLogin")
    print("-register: \tRegister")
    print("-exit: \t\tExit")
    command = input("#en> ")
    
    if command == "-login":
        username = input("Username: ")
        password = input("Password: ")

        #get all user data/pubkey/n
        url = "http://127.0.0.1:8000/user"
        response = requests.get(
            url=url,
            auth=HTTPBasicAuth(username=username,password=password)
            )
        if not response.ok:
            print("Wrong username or password")
            continue

        user_objs = response.json()

        while True:
            # get all images of user
            url = "http://127.0.0.1:8000/user/images"

            response = requests.get(
                url=url,
                auth=HTTPBasicAuth(username=username,password=password)
                )
            e = None
            n = None
            for user in user_objs:
                if username==user['username']:
                    e = user['public_key']
                    n = user['n']

            img_objs = response.json()
            if(len(img_objs)):
                print("Your images: ")
                for img_obj in img_objs:
                    print('\t' + img_obj['image'].split('/')[-1])
            else:
                print("You have no image")

            print("")
            print("-upload: \tUpload Image")
            print("-down: \t\tDownload Image")
            print("-share: \tShare Image")
            print("-ls: \t\tList Image")
            print("-ret: \t\tReturn")
            command = input("#en> ")

            if command == "-upload":
                # upload images
                # params: username, password, image
                url = "http://127.0.0.1:8000/user/images"

                path_to_image = input("Path to image: ")
                filename = path_to_image.split('/')[-1]


                session_key = random.randint(0, 256)
                encrypted_session_key = RSA.power_mod(session_key, e, n)

                try:
                    Encryption.encrypt_image(path_to_image, filename,session_key)
                except:
                    print("File not found")
                    continue

                files = {'image': open(filename,'rb')}
                data = {'encrypted_session_key':encrypted_session_key}

                response = requests.post(
                    url=url,
                    auth=HTTPBasicAuth(username=username,password=password),
                    files=files,
                    data=data
                    )
                if response.status_code == 201:
                    print("Upload successfully")
                    break
                
            elif command == "-down":
                if(len(img_objs)):
                    img_name = input("Input image name to download: ")
                    img_id = None
                    encrypted_session_key = None
                    prv_key = None

                    for img_obj in img_objs:
                        if img_name == img_obj['image'].split('/')[-1]:
                            img_id = img_obj['id']
                            encrypted_session_key = img_obj['encrypted_session_key']
                    if img_id:
                        response = requests.get(url=url+f"/{img_id}", stream=True, auth=HTTPBasicAuth(username=username,password=password))
                        
                        if response.status_code == 302:
                            with open(img_name, 'wb') as handle:
                                for block in response.iter_content(1024):
                                    if not block:
                                        break
                                    handle.write(block)
                            with open(f"{username}_key.txt","r") as prv_key_file:
                                prv_key = int(prv_key_file.read())
                                session_key = RSA.power_mod(encrypted_session_key, prv_key, n)
                                Encryption.encrypt_image(img_name, img_name, session_key)

                            print("Download and decrypt successfully")
                    else:
                        print(f"You have no image name '{img_name}'")

                else:
                    print("You have no image")

            elif command == "-share":
                if(len(img_objs)):
                    img_id = None
                    encrypted_session_key = None

                    url = "http://127.0.0.1:8000/user/images/share"
                    target = input("Input username you want to share image to: ")
                    img_name = input("Input your image name you want to share: ")
                    for img_obj in img_objs:
                        if img_name == img_obj['image'].split('/')[-1]:
                            img_id = img_obj['id']
                            encrypted_session_key = img_obj['encrypted_session_key']
                    if not img_id:
                        print(f"You have no image name '{img_name}'")
                        continue

                    payload = {
                        "target_username":target,
                    }

                    r = requests.get(
                        url=url,
                        params=payload,
                        auth=HTTPBasicAuth(username=username,password=password)
                    )

                    if r.ok:
                        data = r.json()
                        target_pub_key = int(data['target_pub_key'])
                        target_user_n = int(data['target_user_n'])

                        with open(f"{username}_key.txt","r") as prv_key_file:
                            prv_key = int(prv_key_file.read())
                            session_key = RSA.power_mod(encrypted_session_key, prv_key, n)
                        re_encrypted_key = RSA.power_mod(session_key, target_pub_key, target_user_n)

                        payload = {
                            "re_encrypted_key":re_encrypted_key,
                            "img_id":img_id,
                            "target_username":target,
                        }

                        r = requests.post(
                        url=url,
                        data=payload,
                        auth=HTTPBasicAuth(username=username,password=password)
                        )

                        if response.ok:
                            print("Share successfully")
                    else:
                        print(f"There is no username '{username}'")

                else:
                    print("You have no image")

            elif command == "-ls":
                if(len(img_objs)):
                    print("Your images: ")
                    for img_obj in img_objs:
                        print('\t' + img_obj['image'].split('/')[-1])
                else:
                    print("You have no image")

            elif command == "-ret":
                break

            else:
                print(f"{command} is not regconized")

    elif command == "-register":
        # register
        # params: username, password, public key
        url = "http://127.0.0.1:8000/user/register"

        e, d, n, z ,p , q = RSA.generate_key_pair(16)
        username = input("Username: ")
        password = input("Password: ")
        public_key = e
        signature = RSA.power_mod(Encryption.hash_string(username), d, n)
        obj = {
            'username':username,
            'password':password,
            'public_key':public_key,
            'signature':signature,
            'n':n
        }
        response = requests.post(
            url=url,
            json=obj
            )
        if response.status_code == 201:
            with open(f"{username}_key.txt","w") as prv_key_file:
                prv_key_file.write(str(d))

    elif command == "-exit":
        break

    else:
        print(f"{command} is not regconized")

