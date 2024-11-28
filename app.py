from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from backend import PlaylistManager, UserManager, AdminManager, Video, Playlist
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
playlist_manager = PlaylistManager()
user_manager = UserManager()
admin_manager = AdminManager()

# ----------------------
# Route: Trang chính
# ----------------------
@app.route('/', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        choice = request.form['choice']
        
        # Xử lý đăng nhập admin
        if choice == 'admin':
            if admin_manager.sign_in(username, password):
                session['admin'] = username
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('admin_menu'))
            else:
                # Thông báo lỗi khi thông tin admin không chính xác
                flash('Tên đăng nhập hoặc mật khẩu không chính xác.', 'danger')
                return render_template('home.html')
        
        # Xử lý đăng nhập user
        else:
            user = user_manager.get_user_by_username(username)
            if user and user.password == password:
                if user.check == "VALID":
                    session['user'] = username
                    try:
                        session['user_id'] = int(user.ID)  # Lưu ID người dùng vào session
                        flash('Đăng nhập thành công!', 'success')
                        return redirect(url_for('user_menu'))
                    except ValueError as e:
                        flash('Lỗi khi lấy ID người dùng.', 'danger')
                        print(f"Error parsing user ID: {user.ID}, error: {e}")
                else:
                    flash('Tài khoản của bạn đã bị cấm.', 'danger')
            else:
                # Thông báo lỗi khi thông tin user không chính xác
                flash('Tên đăng nhập hoặc mật khẩu không hợp lệ.', 'danger')
                return render_template('home.html')
    
    return render_template('home.html')

# ----------------------
# Đăng ký
# ----------------------
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        sdt = request.form['sdt']
        choice = request.form.get('choice', 'user')  # Mặc định là user nếu không có
        
        # Xử lý đăng ký người dùng
        if user_manager.sign_up_user(username, password, email, sdt):
            flash('Đăng ký người dùng thành công! Bạn có thể đăng nhập.', 'success')
            return redirect(url_for('show'))
        else:
            flash('Tên đăng nhập đã tồn tại.', 'danger')

    return render_template('sign_up.html')


# ----------------------
# Đăng xuất
# ----------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    session.pop('user_id', None)  # Xóa ID người dùng khỏi session
    flash('Đăng xuất thành công.', 'success')
    return redirect(url_for('show'))

# ----------------------
# Hiển thị menu người dùng
# ----------------------
@app.route('/user_menu')
def user_menu():
    if 'user' not in session:
        flash('Bạn cần đăng nhập để truy cập menu người dùng.', 'danger')
        return redirect(url_for('sign_in'))
    return render_template('user_menu.html')

# ----------------------
# Tạo playlist
# ----------------------
@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    if 'user' not in session:
        flash('Bạn cần đăng nhập để tạo playlist.', 'danger')
        return redirect(url_for('sign_in'))

    user_id = session['user_id']  # Lấy ID người dùng từ session
    has_playlist = playlist_manager.check_user_playlist(user_id)  # Kiểm tra user đã có playlist chưa

    if request.method == 'POST':
        tacgia = request.form['tacgia']
        mota = request.form['mota']
        danhgia = request.form['danhgia']
        status = request.form['status']  # Lấy trạng thái từ form
        list_videos = []

        for i in range(1, 6):  # Lấy tối đa 5 video
            chude = request.form.get(f'chude_{i}')
            link = request.form.get(f'link_{i}')
            if chude and link:
                list_videos.append(Video(chude, link))

        playlist = Playlist(user_id, tacgia, mota, danhgia, list_videos, status)
        playlist_manager.write_playlist_to_text(playlist, user_id, has_playlist)
        
        flash('Playlist mới đã được tạo và thay thế Playlist cũ!', 'success')
        return redirect(url_for('user_menu'))  # Quay về menu user sau khi tạo

    return render_template('create_playlist.html', has_playlist=has_playlist)
# ----------------------
# Hiển thị playlist
# ----------------------
@app.route('/show_playlist', methods=['GET', 'POST'])
def show_playlist():
    if 'user' not in session:
        flash('Bạn cần đăng nhập để xem playlist.', 'danger')
        return redirect(url_for('sign_in'))

    user_id = session['user_id']
    playlists = playlist_manager.get_user_playlists(user_id)
    playlist = next((p for p in playlists if p.ID == str(user_id)), None)

    video_url = None
    if request.method == 'POST':
        video_index = int(request.form['video_index']) - 1
        if playlist and 0 <= video_index < len(playlist.list_videos):
            video_url = playlist.list_videos[video_index].link
            if "youtube.com" in video_url or "youtu.be" in video_url:
                video_url = convert_to_embed_url(video_url)
            flash('Đang phát video!', 'success')
        else:
            flash('Chỉ số video không hợp lệ.', 'danger')

    return render_template('show_playlist.html', playlists=playlists, playlist=playlist, video_url=video_url)

def convert_to_embed_url(url):
    if "youtube.com" in url:
        video_id = url.split("v=")[1]
        ampersand_position = video_id.find("&")
        if ampersand_position != -1:
            video_id = video_id[:ampersand_position]
        return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be" in url:
        video_id = url.split("/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return url

# ----------------------
# Thêm video vào playlist
# ----------------------
@app.route('/add_video', methods=['GET', 'POST'])
def add_video():
    if 'user' not in session:
        flash('Bạn cần đăng nhập để thêm video vào playlist.', 'danger')
        return redirect(url_for('sign_in'))
    
    user_id = session['user_id']  # Lấy ID người dùng từ session
    playlist = playlist_manager.get_user_playlist(user_id)  # Lấy playlist của người dùng

    if not playlist:
        flash('Playlist không tồn tại.', 'danger')
        return redirect(url_for('user_menu'))

    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('user_menu'))
        
        chude = request.form['chude']
        link = request.form['link']
        new_video = Video(chude, link)
        playlist.list_videos.append(new_video)
        playlist_manager.write_playlist_to_text(playlist, user_id, True)
        flash('Video đã được thêm vào playlist!', 'success')
        return redirect(url_for('user_menu'))
    
    return render_template('add_video.html')

# ----------------------
# Xóa video khỏi playlist
# ----------------------
@app.route('/delete_video', methods=['GET', 'POST'])
def delete_video():
    if 'user' not in session:
        flash('Bạn cần đăng nhập để xóa video khỏi playlist.', 'danger')
        return redirect(url_for('sign_in'))

    user_id = session['user_id']  # Lấy ID người dùng từ session
    playlist = playlist_manager.get_user_playlist(user_id)  # Lấy playlist của người dùng

    if not playlist:
        flash('Playlist không tồn tại.', 'danger')
        return redirect(url_for('user_menu'))

    if request.method == 'POST':
        video_index = int(request.form['video_index']) - 1  # Lấy chỉ số video từ form
        if 0 <= video_index < len(playlist.list_videos):
            del playlist.list_videos[video_index]  # Xóa video khỏi danh sách
            playlist_manager.write_playlist_to_text(playlist, user_id, True)  # Cập nhật lại file
            flash('Video đã được xóa khỏi playlist!', 'success')
        else:
            flash('Chỉ số video không hợp lệ.', 'danger')
        return redirect(url_for('delete_video'))

    return render_template('delete_video.html', playlist=playlist)
# ----------------------
# Cập nhật playlist
# ----------------------
@app.route('/update_playlist', methods=['GET', 'POST'])
def update_playlist():
    if 'user' not in session:
        flash('Bạn cần đăng nhập để cập nhật playlist.', 'danger')
        return redirect(url_for('sign_in'))

    user_id = session['user_id']  # Lấy ID người dùng từ session
    playlist = playlist_manager.get_user_playlist(user_id)  # Lấy playlist của người dùng

    if not playlist:
        flash('Playlist không tồn tại.', 'danger')
        return redirect(url_for('user_menu'))

    if request.method == 'POST':
        tacgia = request.form['tacgia']
        mota = request.form['mota']
        danhgia = request.form['danhgia']
        status = request.form['status']  # Lấy trạng thái từ form

        # Cập nhật thông tin playlist
        playlist.tacgia = tacgia
        playlist.mota = mota
        playlist.danhgia = danhgia
        playlist.status = status  # Cập nhật trạng thái

        # Ghi lại playlist đã cập nhật vào file
        playlist_manager.write_playlist_to_text(playlist, user_id, True)
        
        flash('Playlist đã được cập nhật thành công!', 'success')
        return redirect(url_for('user_menu'))  # Quay về menu user sau khi cập nhật

    return render_template('edit_playlist.html', playlist=playlist)


@app.route('/public_playlists', methods=['GET', 'POST'])
def public_playlists():
    if 'user' not in session:
        flash('Bạn cần đăng nhập để xem các playlist công khai.', 'danger')
        return redirect(url_for('sign_in'))

    user_id = session['user_id']
    playlists = playlist_manager.get_public_playlists(user_id)
    selected_playlist = None
    video_url = None

    if request.method == 'POST':
        if 'playlist_id' in request.form:
            playlist_id = request.form['playlist_id']
            for playlist in playlists:
                if playlist.ID == playlist_id:
                    selected_playlist = playlist
                    break
        elif 'video_index' in request.form:
            playlist_id = request.form['selected_playlist_id']
            video_index = int(request.form['video_index']) - 1
            for playlist in playlists:
                if playlist.ID == playlist_id:
                    selected_playlist = playlist
                    if 0 <= video_index < len(playlist.list_videos):
                        video_url = playlist.list_videos[video_index].link
                        video_url = convert_to_embed_url(video_url)
                    break

    return render_template('public_playlists.html', playlists=playlists, selected_playlist=selected_playlist, video_url=video_url)

# ----------------------
# Hiển thị menu admin
# ----------------------
@app.route('/admin_menu')
def admin_menu():
    if 'admin' not in session:
        flash('Bạn cần đăng nhập để truy cập menu admin.', 'danger')
        return redirect(url_for('sign_in'))
    return render_template('admin_menu.html')

# ----------------------
# Hiển thị playlist
# ----------------------
@app.route('/admin_show_playlist')
def admin_show_playlist():
    if 'admin' not in session:
        flash('Bạn cần đăng nhập với tư cách admin để xem playlist.', 'danger')
        return redirect(url_for('sign_in'))
    playlists = playlist_manager.get_all_playlists()
    playlists = sorted(playlists, key=lambda p: int(p.ID)) 
    return render_template('admin_show_playlist.html', playlists=playlists)
# ----------------------
# Hiển thị người dùng
# ----------------------
@app.route('/admin_show_users')
def admin_show_users():
    if 'admin' not in session:
        flash('Bạn cần đăng nhập để xem người dùng.', 'danger')
        return redirect(url_for('sign_in'))
    users = user_manager.read_list_user_from_text()
    users = sorted(users, key=lambda u: int(u.ID))
    return render_template('show_users.html', users=users)

# ----------------------
# Xóa playlist
# ----------------------
@app.route('/admin_delete_playlist', methods=['GET', 'POST'])
def admin_delete_playlist():
    if 'admin' not in session:
        flash('Bạn cần đăng nhập với tư cách admin để xóa playlist.', 'danger')
        return redirect(url_for('sign_in'))

    if request.method == 'POST':
        playlist_id = request.form['playlist_id']
        playlists = playlist_manager.get_all_playlists()
        playlist_to_delete = None

        for playlist in playlists:
            if playlist.ID == playlist_id:
                playlist_to_delete = playlist
                break

        if playlist_to_delete:
            playlist_manager.delete_playlist_from_text(playlist_to_delete)
            flash('Playlist đã được xóa thành công!', 'success')
        else:
            flash('Không tìm thấy playlist.', 'danger')

        return redirect(url_for('admin_delete_playlist'))

    playlists = playlist_manager.get_all_playlists()
    return render_template('delete_playlist.html', playlists=playlists)
# ----------------------
# Ban/Unban người dùng
# ----------------------
@app.route('/admin_ban_unban_user', methods=['GET', 'POST'])
def admin_ban_unban_user():
    if 'admin' not in session:
        flash('Bạn cần đăng nhập để ban/unban người dùng.', 'danger')
        return redirect(url_for('sign_in'))
    if request.method == 'POST':
        user_id = request.form['user_id']
        users = user_manager.read_list_user_from_text()
        user = next((u for u in users if u.ID == user_id), None)
        if user:
            if user.check == "VALID":
                user_manager.ban_user(user)
                flash('Người dùng đã bị cấm!', 'success')
            else:
                user_manager.unban_user(user)
                flash('Người dùng đã được bỏ cấm!', 'success')
        else:
            flash('Người dùng không tồn tại.', 'danger')
        return redirect(url_for('admin_ban_unban_user'))
    users = user_manager.read_list_user_from_text()
    users = sorted(users, key=lambda u: int(u.ID))
    return render_template('ban_unban_user.html', users=users)


def print_playlist_to_monitor(playlist):
    print("------------")
    print("ID: " + str(playlist.ID))
    print("Tác giả: " + playlist.tacgia)
    print("Mô tả: " + playlist.mota)
    print("Đánh giá: " + playlist.danhgia)
    print_videos(playlist.list_videos)
    print("------------")

def print_videos(list_videos):
    for video in list_videos:
        print("Chủ đề: " + video.chude)
        print("Link: " + video.link)

# ----------------------
# Chạy ứng dụng Flask
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)