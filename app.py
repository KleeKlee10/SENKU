from flask import Flask, render_template, request

app = Flask(__name__)

# Bảng quy đổi điểm hệ 10 sang điểm chữ
bang_diem_he_10 = {
    'F': (0.0, 4.0),
    'D': (4.0, 5.0),
    'D+': (5.0, 5.5),
    'C': (5.5, 6.5),
    'C+': (6.5, 7.0),
    'B': (7.0, 8.0),
    'B+': (8.0, 8.5),
    'A': (8.5, 9.5),
    'A+': (9.5, 10.1),
}

# Bảng quy đổi điểm chữ sang điểm hệ 4
bang_diem_he_4 = {
    'F': 0.0,
    'D': 1.0,
    'D+': 1.5,
    'C': 2.0,
    'C+': 2.5,
    'B': 3.0,
    'B+': 3.5,
    'A': 4.0,
    'A+': 4.0,
}

# Chuyển đổi điểm hệ 10 sang điểm chữ
def tinh_diem_chu(diem):
    for grade, (low, high) in bang_diem_he_10.items():
        if low <= diem < high:
            return grade
    return None  # Trả về None nếu không tìm thấy

# Chuyển điểm chữ sang điểm hệ 4
def tinh_diem_he_4(diem_chu):
    if diem_chu in bang_diem_he_4:
        return bang_diem_he_4[diem_chu]
    else:
        return None  # Trả về None nếu điểm chữ không hợp lệ

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ten_mon_hoc = request.form.getlist('course_name')
        diem = list(map(float, request.form.getlist('score')))
        tin_chi = list(map(int, request.form.getlist('credits')))

        diem_chus = []
        diem_he_4_list = []
        
        for d in diem:
            diem_chu = tinh_diem_chu(d)  # Chuyển đổi điểm hệ 10 sang điểm chữ
            diem_chus.append(diem_chu)
            diem_he_4 = tinh_diem_he_4(diem_chu)  # Chuyển đổi điểm chữ sang điểm hệ 4
            
            if diem_he_4 is None:
                return render_template('error.html', message="Điểm chữ không hợp lệ.")  # Trả về trang lỗi
            
            diem_he_4_list.append(diem_he_4)

        # Tính điểm trung bình hệ 10
        diem_trung_binh_he_10 = sum(d * c for d, c in zip(diem, tin_chi)) / sum(tin_chi) if sum(tin_chi) > 0 else 0
        diem_trung_binh_he_10 = round(diem_trung_binh_he_10, 2)

        # Tính điểm trung bình hệ 4 từ điểm hệ 4
        diem_trung_binh_he_4 = sum(d * c for d, c in zip(diem_he_4_list, tin_chi)) / sum(tin_chi) if sum(tin_chi) > 0 else 0
        diem_trung_binh_he_4 = round(diem_trung_binh_he_4, 1)

        # Xác định loại học lực
        loai_hoc_luc = ''
        if diem_trung_binh_he_4 >= 3.6:
            loai_hoc_luc = 'Xuất Sắc'
        elif diem_trung_binh_he_4 >= 3.2:
            loai_hoc_luc = 'Giỏi'
        elif diem_trung_binh_he_4 >= 2.5:
            loai_hoc_luc = 'Khá'
        elif diem_trung_binh_he_4 >= 2.0:
            loai_hoc_luc = 'Trung Bình'
        elif diem_trung_binh_he_4 >= 1.0:
            loai_hoc_luc = 'Yếu'
        else:
            loai_hoc_luc = 'Kém'

        return render_template('result.html', ten_mon_hoc=ten_mon_hoc, diem=diem, tin_chi=tin_chi,
                               diem_chus=diem_chus, diem_he_4_list=diem_he_4_list,
                               diem_trung_binh_he_10=diem_trung_binh_he_10,
                               diem_trung_binh_he_4=diem_trung_binh_he_4, loai_hoc_luc=loai_hoc_luc)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
