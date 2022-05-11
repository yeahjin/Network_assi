# Assignment for Computer Network Lectures in Spring 2021

1. First Assignment - Implementing a simple web browser

    간단한 웹브라우저 구현이다.
    파일을 다운로드 하는 명령어는 'get'이다.
    
    ```c
    get url
    ```
    
    quit 명령은 프로그램을 끝낸다.
    
    ```c
    quit
    ```
    
    이 파일의 URL에서 실제 파일을 찾아낸 다음 그 파일 이름으로 local에 저장한다.
    
2. Second Assignment - Implementing a simple web server
    
    간단한 웹서버를 구현한다.
    웹서버 프로그램인 hw2를 실행할 때, parameter로 port number를 제공한다.
    
    ```c
    $hw2 portnumber
    ```
    
    그 다음 웹브라우저를 실행해서 파일을 요청한다.
    같은 호스트웨어 요청하기 때문에 도메인 이름은 localhost를 사용한다.
    
    ```c
    [http://localhost](http://localhost/):portnumber/xxx.html
    ```
    
    브라우저에 위의 URL를 입력하면 xxx.html파일을 서버로 요청한다.
    그러고 파일을 받으면 웹브라우저 화면에 보여준다.
    
3. Third Assignment - Implementing a group chat server

    단체 채팅 서버를 구현한다. 채팅 client는 telnet으로 대체한다. 이 서버 프로그램은 tcp port 번호를 command line argument로 입력받아 시작한다. 즉 이 응용프로그램을 실행할 때 1개의 argument를 입력받아야 한다.
    
    ```c
    $hw3 tcpport
    ```
    
    - tcpport: client로부터 들어오는 connetion request를 받기 위한 TCP port number

4.  Fourth Assignment - Implementing a simple two-person chat program

    간단한 2인 채팅 프로그램이다.
    이 응용 프로그램은 사용자로부터 포트 번호와 아이디를 입력받아 시작한다.
    
    ```c
    @talk hostname tcpport
    ```
    
    - tcpport: 상대방 프로그램의 포트 번호
    - hostname: 상대방 컴퓨터의 이름