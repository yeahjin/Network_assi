from socket import *

# https://stackoverflow.com/questions/43408325/how-to-download-image-from-http-server-python-sockets
# 학번,이름

while True:
    geturl = input()
    if geturl == "quit":
        break
    geturl = geturl.split(" ") #get
    get_info_get = geturl[0] # get
    if get_info_get != "get":
        print("Only support get")
        continue

    if len(geturl) != 2:
        print("Incorrect Input\n")
        continue

    geturl = geturl[1] #url만 빼온다.
    get_url_list = geturl.split("/")
    url_info_url = get_url_list[2] # host
    url_info_photo_name = get_url_list[-1] #사진이름
    url_info_prtc = get_url_list[0][:-1] # http 추출
    serverPort = 80

    if url_info_prtc == "http":
        serverPort = 80
    elif url_info_prtc == "https":
        print("Only support http, not https\n")
        continue
    else:
        print("Only support http. not "+url_info_prtc+" \n" )
        continue

    # host에 ":"유무 판별뒤 url와 port num나눈다.
    strnum = url_info_url.find(":")
    if strnum >= 0:
        a = url_info_url.split(":")
        serverPort = int(a[1])
        url_info_url = a[0]

    try: # 서버에 연결할 수 없는 경우 예외 처리
        host_ip_addr = gethostbyname(url_info_url)

    except gaierror as e:
        print(url_info_prtc +" " +url_info_url+" " + url_info_url+" " + str(serverPort)+" " + url_info_photo_name)
        print(url_info_url + " : unknown host")
        print("cannot connect to server " + url_info_url+" " +str(serverPort)+"\n")

    else:
        clientSocket = socket(AF_INET, SOCK_STREAM) #소켓생성
        clientSocket.connect((host_ip_addr,serverPort))

        cmd = "GET " +geturl + " " +"HTTP/1.0\r\n\r\n"
        clientSocket.send(cmd.encode())
        total_size = 0
        al = []
        asdf = ""
        cnt = 0
        while True:
            a = clientSocket.recv(1)
            if len(a) < 1:
                break
            cnt += 1
            if cnt <= 4:
                al.append(a.decode())
                asdf += a.decode()
            else:
                al[0], al[1], al[2] = al[1], al[2], al[3]
                al[3] = a.decode()
                asdf += a.decode()
            if al[0] == "\r" and al[1] == '\n' and al[2] == "\r" and al[3] == "\n":
                break

        nf = ""
        agasd = asdf.split("\r\n")
        httpverion = ""
        connectionS = ""
        for i in agasd:
            contentL =  i.find("Content-Length: ")
            httpV = i.find("HTTP/")
            connectionstate=i.find("Connection: ")
            if contentL >= 0:
                total_size = int(i[16:])
            elif httpV >= 0:
                httpverion = i[:9]
                nf = i[9:]
            elif connectionstate>=0:
                connectionS = i[:]

        if nf == "200 OK":
            print("GET " + '/'.join(get_url_list[3:])+" "+httpverion+"\r")
            print("Host: %s\r" %(url_info_url))
            print("User-agent : HW1/1.0\r")
            print(connectionS+"\r\n\r\n")

            print("total size: ", total_size)

            image_bin = b''
            total = 0
            l = [1,2,3,4,5,6,7,8,9,10]
            while True: # 수신받을 수 있는 루프
                data = clientSocket.recv(1024) # 1024는 버퍼의 크기
                if total_size > total:
                    total += len(data)
                    abcd = int(total/total_size*100)//10
                    if abcd in l:
                        print("Current Downloading %d/%d (bytes) %d%%" % (total,total_size,total/total_size*100))
                        l.remove(abcd)
                    image_bin += data
                else:
                    print("Download Complete: %s, %d/%d\n"%(url_info_photo_name,total,total_size))
                    break

            image = image_bin[:]

            f = open(url_info_photo_name,'wb')
            f.write(image)
            f.close()

            clientSocket.close()

        else:
            print(nf)
            continue


