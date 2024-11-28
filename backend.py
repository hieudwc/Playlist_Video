import webbrowser
import csv
import os
import shutil

class Video:
    def __init__(self, chude, link):
        self.chude = chude
        self.link = link

    def open(self):
        webbrowser.open(self.link)

class Playlist:
    def __init__(self, ID, tacgia, mota, danhgia, list_videos, status):
        self.ID = ID
        self.tacgia = tacgia
        self.mota = mota
        self.danhgia = danhgia
        self.list_videos = list_videos
        self.status = status

class User:
    def __init__(self, ID, username, password, email, sdt, check):
        self.ID = ID
        self.username = username
        self.password = password
        self.email = email
        self.sdt = sdt
        self.check = check

class Admin:
    def __init__(self, ID, username, password, email, sdt):
        self.ID = ID
        self.username = username
        self.password = password
        self.email = email
        self.sdt = sdt

class PlaylistManager:
    
    @staticmethod
    def get_public_playlists(user_id):
        list_playlist = []
        with open("playlist.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split("</>")
                    try:
                        ID = data[0]
                        tacgia = data[1]
                        mota = data[2]
                        danhgia = data[3]
                        status = data[-1]  # Trạng thái ở cuối
                        if status == "public" and ID != str(user_id):
                            list_videos = PlaylistManager.read_videos_from_text(data[4:-1])
                            playlist = Playlist(ID, tacgia, mota, danhgia, list_videos, status)
                            list_playlist.append(playlist)
                    except ValueError as e:
                        print(f"Error parsing line: {line}, error: {e}")
        return list_playlist

    @staticmethod
    def get_user_playlist(user_id):
        with open("playlist.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split("</>")
                    try:
                        if data[0] == str(user_id):
                            ID = data[0]
                            tacgia = data[1]
                            mota = data[2]
                            danhgia = data[3]
                            status = data[-1]  # Trạng thái ở cuối
                            list_videos = PlaylistManager.read_videos_from_text(data[4:-1])
                            return Playlist(ID, tacgia, mota, danhgia, list_videos, status)
                    except ValueError as e:
                        print(f"Error parsing line: {line}, error: {e}")
        return None
    
    @staticmethod
    def get_user_playlists(user_id):
        list_playlist = []
        with open("playlist.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split("</>")
                    try:
                        if data[0] == str(user_id):
                            ID = data[0]
                            tacgia = data[1]
                            mota = data[2]
                            danhgia = data[3]
                            status = data[-1]  # Trạng thái ở cuối
                            list_videos = PlaylistManager.read_videos_from_text(data[4:-1])
                            playlist = Playlist(ID, tacgia, mota, danhgia, list_videos, status)
                            list_playlist.append(playlist)
                    except ValueError as e:
                        print(f"Error parsing line: {line}, error: {e}")
        return list_playlist

    @staticmethod
    def get_all_playlists():
        list_playlist = []
        with open("playlist.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split("</>")
                    try:
                        ID = data[0]
                        tacgia = data[1]
                        mota = data[2]
                        danhgia = data[3]
                        status = data[-1]  # Trạng thái ở cuối
                        list_videos = PlaylistManager.read_videos_from_text(data[4:-1])
                        playlist = Playlist(ID, tacgia, mota, danhgia, list_videos, status)
                        list_playlist.append(playlist)
                    except ValueError as e:
                        print(f"Error parsing line: {line}, error: {e}")
        return list_playlist

    @staticmethod
    def read_playlist_from_text():
        list_playlist = []
        with open("playlist.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split("</>")
                    try:
                        ID = data[0]
                        tacgia = data[1]
                        mota = data[2]
                        danhgia = data[3]
                        status = data[4]
                        list_videos = PlaylistManager.read_videos_from_text(file, data)
                        playlist = Playlist(ID, tacgia, mota, danhgia, list_videos, status)
                        list_playlist.append(playlist)
                    except ValueError as e:
                        print(f"Error parsing line: {line}, error: {e}")
        return list_playlist

    @staticmethod
    def read_videos_from_text(data):
        list_videos = []
        try:
            slg = int(data[0])
            k = 1
            for i in range(slg):
                chude = data[k]
                link = data[k + 1]
                k += 2
                video = Video(chude, link)
                list_videos.append(video)
        except ValueError as e:
            print(f"Error parsing videos: {data}, error: {e}")
        return list_videos

    @staticmethod
    def write_videos_to_text(list_videos, file):
        for video in list_videos:
            file.write(video.chude + "</>")
            file.write(video.link + "</>")

    @staticmethod
    def write_playlist_to_text(playlist, user_id, check):
        if check:
            with open("playlist.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
            with open("playlist.txt", "w", encoding="utf-8") as file:
                if file.tell() != 0:
                    file.write("\n")
                found = False
                for line in lines:
                    if line.startswith(str(user_id) + "</>"):
                        file.write(str(user_id) + "</>")
                        file.write(playlist.tacgia + "</>")
                        file.write(playlist.mota + "</>")
                        file.write(playlist.danhgia + "</>")
                        file.write(str(len(playlist.list_videos)) + "</>")
                        PlaylistManager.write_videos_to_text(playlist.list_videos, file)
                        file.write(playlist.status + "\n")
                        found = True
                    else:
                        file.write(line)
                if found:
                    print("Đã cập nhật thông tin playlist thành công!")
        else:
            with open("playlist.txt", "a", encoding="utf-8") as file:
                if file.tell() != 0:
                    file.write("\n")
                file.write(str(user_id) + "</>")
                file.write(playlist.tacgia + "</>")
                file.write(playlist.mota + "</>")
                file.write(playlist.danhgia + "</>")
                file.write(str(len(playlist.list_videos)) + "</>")
                PlaylistManager.write_videos_to_text(playlist.list_videos, file)
                file.write(playlist.status + "\n")
            print("Đã tạo playlist mới thành công!")
            
    @staticmethod
    def check_user_playlist(user_id):
        with open("playlist.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith(str(user_id) + "</>"):
                    return True
        return False

    @staticmethod
    def delete_playlist_from_text(playlist):
        with open("playlist.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("playlist.txt", "w", encoding="utf-8") as file:
            for line in lines:
                if not line.startswith(playlist.ID + "</>"):
                    file.write(line)

    @staticmethod
    def play_video(playlist, video_index):
        if 0 <= video_index < len(playlist.list_videos):
            video = playlist.list_videos[video_index]
            print(f"Open video {video_index + 1}: {video.chude} - {video.link}")
            video.open()
        else:
            print("Invalid video index")
            
    @staticmethod
    def add_video(playlist):
        print("Enter video name and link:")
        new_video = PlaylistManager.read_video_from_keyboard()
        playlist.list_videos.append(new_video)
        return playlist

    @staticmethod
    def update_playlist(playlist):
        print("Bạn muốn sửa phần nào của playlist?")
        print("1. Tác giả.")
        print("2. Mô tả.")
        print("3. Đánh giá.")
        choice = PlaylistManager.select_in_range("Nhập vào phần bạn muốn sửa (1-3): ", 1, 3)
        if choice == 1:
            new_tacgia = input("Nhập vào tên tác giả mới: ")
            playlist.tacgia = new_tacgia
            print("Update successfully!")
        elif choice == 2:
            new_mota = input("Nhập vào mô tả mới: ")
            playlist.mota = new_mota
            print("Update successfully!")
        elif choice == 3:
            new_danhgia = input("Nhập vào đánh giá mới: ")
            playlist.danhgia = new_danhgia
            print("Update successfully!")
        return playlist

    @staticmethod
    def delete_video(playlist):
        PlaylistManager.print_videos(playlist.list_videos)
        choice = PlaylistManager.select_in_range("Nhập video muốn xóa (1-" + str(len(playlist.list_videos)) + "): ", 1, len(playlist.list_videos))
        del playlist.list_videos[choice - 1]
        print("Đã xóa video thành công!")
        return playlist

    @staticmethod
    def read_video_from_keyboard():
        chude = input("Nhập chủ đề video: ")
        link = input("Nhập link video: ")
        return Video(chude, link)

    @staticmethod
    def print_videos(list_videos):
        print("Danh sách video:")
        for i, video in enumerate(list_videos, start=1):
            print(f"- Video {i} :")
            print(f"    Chủ đề: {video.chude}")
            print(f"    Link: {video.link}")

    @staticmethod
    def select_in_range(prompt, min, max):
        choice = input(prompt)
        while not choice.isdigit() or not (min <= int(choice) <= max):
            print("Lỗi! Hãy nhập lại!")
            choice = input(prompt)
        return int(choice)

class UserManager:
    @staticmethod
    def sign_up_user(username, password, email, sdt):
        list_user = UserManager.read_list_user_from_text()
        for user in list_user:
            if user.username == username:
                return False  # Tên người dùng đã tồn tại
        n = len(list_user)
        ID = n + 1
        check = "VALID"
        user = User(ID, username, password, email, sdt, check)
        UserManager.save_user(user)
        return True

    @staticmethod
    def save_user(user):
        # Tạo file nếu chưa tồn tại
        if not os.path.exists("user.txt"):
            with open("user.txt", "w", encoding="utf-8") as file:
                pass

        with open("user.txt", "a", encoding="utf-8") as file:
            if file.tell() != 0:
                file.write("\n")
            file.write(str(user.ID) + "</>")
            file.write(user.username + "</>")
            file.write(user.password + "</>")
            file.write(user.email + "</>")
            file.write(user.sdt + "</>")
            file.write(user.check)

    @staticmethod
    def read_list_user_from_text():
        list_user = []
        # Tạo file nếu chưa tồn tại
        if not os.path.exists("user.txt"):
            with open("user.txt", "w", encoding="utf-8") as file:
                pass

        with open("user.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split("</>")
                    ID = data[0]
                    username = data[1]
                    password = data[2]
                    email = data[3]
                    sdt = data[4]
                    check = data[5]
                    user = User(ID, username, password, email, sdt, check)
                    list_user.append(user)
        return list_user

    @staticmethod
    def sign_in(username, password):
        list_user = UserManager.read_list_user_from_text()
        for user in list_user:
            if user.username == username and user.password == password and user.check == "VALID":
                return True
        return False
    
    @staticmethod
    def get_user_id(username):
        list_user = UserManager.read_list_user_from_text()
        for user in list_user:
            if user.username == username:
                return user.ID
        return None
    
    @staticmethod
    def get_user_by_username(username):
        list_user = UserManager.read_list_user_from_text()
        for user in list_user:
            if user.username == username:
                return user
        return None

    @staticmethod
    def ban_user(user):
        with open("user.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("user.txt", "w", encoding="utf-8") as file:
            for line in lines:
                if line.startswith(str(user.ID) + "</>") and user.check == "VALID":
                    line = line.replace("VALID", "INVALID")
                file.write(line)
        print("Đã cấm người dùng thành công!")

    @staticmethod
    def unban_user(user):
        with open("user.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("user.txt", "w", encoding="utf-8") as file:
            for line in lines:
                if line.startswith(str(user.ID) + "</>") and user.check == "INVALID":
                    line = line.replace("INVALID", "VALID")
                file.write(line)
        print("Đã bỏ cấm người dùng thành công!")

class AdminManager:
    @staticmethod
    def sign_up_admin(username, password, email, sdt):
        list_admin = AdminManager.read_list_admin_from_text()
        for admin in list_admin:
            if admin.username == username:
                return False  # Tên admin đã tồn tại
        n = len(list_admin)
        ID = n + 1
        admin = Admin(ID, username, password, email, sdt)
        AdminManager.save_admin(admin)
        return True

    @staticmethod
    def save_admin(admin):
        # Tạo file nếu chưa tồn tại
        if not os.path.exists("admin.txt"):
            with open("admin.txt", "w", encoding="utf-8") as file:
                pass

        with open("admin.txt", "a", encoding="utf-8") as file:
            if file.tell() != 0:
                file.write("\n")
            file.write(str(admin.ID) + "</>")
            file.write(admin.username + "</>")
            file.write(admin.password + "</>")
            file.write(admin.email + "</>")
            file.write(admin.sdt)

    @staticmethod
    def read_list_admin_from_text():
        list_admin = []
        # Tạo file nếu chưa tồn tại
        if not os.path.exists("admin.txt"):
            with open("admin.txt", "w", encoding="utf-8") as file:
                pass

        with open("admin.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split("</>")
                    ID = data[0]
                    username = data[1]
                    password = data[2]
                    email = data[3]
                    sdt = data[4]
                    admin = Admin(ID, username, password, email, sdt)
                    list_admin.append(admin)
        return list_admin

    @staticmethod
    def sign_in(username, password):
        list_admin = AdminManager.read_list_admin_from_text()
        for admin in list_admin:
            if admin.username == username and admin.password == password:
                return True
        return False