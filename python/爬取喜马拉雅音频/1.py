import requests

#获取登录页面的cookies
session = requests.Session()
login_page = session.get('https://www.ximalaya.com/passport/login')
cookies = login_page.cookies

#构造登录请求
login_url = 'https://www.ximalaya.com/passport/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}
data = {
    'username': 'your_username',
    'password': 'your_password'
}
session.post(login_url, headers=headers, data=data, cookies=cookies)

#访问音频页面
album_id = 'your_album_id'
audio_url = f'https://www.ximalaya.com/revision/play/album?albumId={album_id}&sort=0&pageSize=30'
audio_page = session.get(audio_url, headers=headers)
audio_data = audio_page.json()

#下载音频
for audio in audio_data['data']['tracksAudioPlay']:
    audio_title = audio['trackName']
    audio_src = audio['src']
    response = session.get(audio_src, stream=True)
    with open(f'{audio_title}.mp3', 'wb') as f:
        f.write(response.content)
