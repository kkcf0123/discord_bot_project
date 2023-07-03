# discord_bot_project
discord.py를 이용한 개인서버용 다기능 디스코드 봇
## 주요 기능

---

- Cog Management
    - cog에 대한 load, unload, reload를 이용하여 간편한 유지보수
- ChatGPT
    - ChatGPT의 API를 호출하여 discord Text Channel에서 채팅할 경우, ChatGPT 사용가능
- Message
    - 특정채널의 메세지 자동 삭제 (조건부)
    - 메세지 삭제
- Role
    - server에 새로 가입한 member에게 역할부여
    - mobile member가 voice channel에 접속할 경우 접속시간제한
    - server member들의 status 조회
- Youtube Notification
    - 알림 받을 Youtube Channel, Discord Text Channel 등록
    - 등록된 Youtube Channel의 새 영상 업로드 알림을 Discord Text Channel로 송신
    - 등록된 Youtbue Channel 삭제
    - 등록된 Youtube Channel 조회
- Twitch Live Streaming Notify
    - 알림 받을 Twitch Channel 등록
    - 등록된 Twitch Channel 삭제
    - 등록된 Twitch Channel 조회
    - 등록된 Twtich Live Streaming의 알림을 Discord Text Channel로 송신
- League of Legend
    - 전적검색
    - Team Fight(내전)
        - 내전대기를 위한 voice channel로 멤버이동
        - lol teamFight 5:5 팀 생성
            - 멤버 랜덤분배
            - 팀에 따른 voice channel 자동 이동
        - lol teamFight 2:2:2 팀 생성
            - 멤버 랜덤분배
            - 팀에 따른 voice channel 자동 이동
