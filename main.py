import requests as re
import time,os


def downlod_wallpaper(query, img_count = 30, path="wallpapers", orientation= "landscape"):
    query_words = query.replace(" ", "%20")
    retry = 0
    new_img_timeout = 60*60
    counter = 0
    count = 0
    while True:
        try:

            url = 'https://api.unsplash.com/photos/random?orientation='+orientation+'&query='+query_words+'&count=30'  # unsplash query url.
            headers = {'Authorization': 'Client-ID 2d4a979f27dbdf7734241d4ebabb2abb2ccde8f4d2b4f63449235af819144ba5'}  # unsplash api auth

            r = re.get(url, headers=headers)
            #print(r.status_code)
            if r.status_code == 200:
                json_data = r.json()
                for json in json_data:
                    download_url = json['urls']['regular']+'&w=1920'
                    f_name = json['description']
                    img = re.get(download_url)
                    #print(json)

                    if img.status_code == 200:
                        try:
                            if f_name !=None :
                                with open(path+"/"+f_name+".jpg", 'wb') as f:
                                    f.write(img.content)
                            elif json['alt_description'] != None :
                                with open(path+"/"+json['alt_description']+".jpg", 'wb') as f:
                                    f.write(img.content)
                        except :

                            with open(path+"/wallpaper_"+json['id']+".jpg", 'wb') as f:
                                f.write(img.content)
                        count += 1
                    print("Image downloaded : ", count)
                    if count >= img_count :
                        break

                counter +=1
                retry = 0
                if counter == 50:
                    time.sleep(new_img_timeout)
                    counter = 0
            else:
                print("Wating for new set of Images (Free version is limited to 1500 images an hour. Downloading will resumes after 1 hour timeout)...")
                time.sleep(new_img_timeout)
                counter = 0

            if count >= img_count:
                print("Download Complete .... ")
                break

        except re.exceptions.Timeout:
            print("No connection. Retrying in", retry, "seconds....")
            time.sleep(retry)
            if retry < 100:
                retry +=5
        except re.exceptions.ConnectionError:
            print("No connection. Retrying in",retry,"seconds....")
            time.sleep(retry)
            if retry < 100:
                retry +=5
        except  re.exceptions as e:
            print("Unknown error : ",e)
            break



if __name__ == "__main__":
    query = input("Enter keywords related to images. (Ex. mountains, beach) : ")

    while 1:
        try :
            dir = input("Enter name of folder to save the images (Folder will be created if does not exists.): ")
            os.mkdir(dir)
            break
        except FileExistsError:
            if input("Floder already exists. Use same folder? (Y: same folder/ n : re-enter folder name) : ") == "Y":
                break
        except:
            print("Invalid folder name. Invalid characters.")

    while 1:
        try:
            img_count = int(input("Enter number of images to Download (Defalut : 30):"))
            if img_count > 0 and img_count <= 10000:
                downlod_wallpaper(query,img_count=img_count,path = dir)
                break
            else:
                print("Enter vaild number between [1,10000].")

        except :
            if input("Non-number value entered. Continue with defalut value 30? (Y/n)") == "Y":
                downlod_wallpaper(query,path=dir)
                break



