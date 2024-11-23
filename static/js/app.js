$(document).ready(function() {
    // Load dữ liệu
    function loadData() {
        $.get("/load_data", function(data) {
            const table = $("#data-table");
            table.empty();
            data.forEach((row, index) => {
                table.append(`
                    <tr>
                        <td>${index + 1}</td>
                        <td>${row.HoTen}</td>
                        <td>${row.NgaySinh}</td>
                        <td>${row.Diem}</td>
                        <td>${row.DieuKien}</td>
                        <td>
                            <button class="btn btn-danger btn-sm" onclick="deleteStudent(${row.rowid})">Xóa</button>
                            <button class="btn btn-warning btn-sm" onclick="updateStudent(${row.rowid})">Sửa</button>
                        </td>
                    </tr>
                `);
            });
        });
    }

    // Thêm sinh viên
    $("#add-student-form").submit(function(e) {
        e.preventDefault();
        const formData = $(this).serializeArray().reduce((obj, item) => {
            obj[item.name] = item.value;
            return obj;
        }, {});
    
        console.log(formData);  // In ra dữ liệu gửi lên
    
        $.ajax({
            url: "/insert_data",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function() {
                alert("Thêm sinh viên thành công!");
                loadData();
            },
            error: function(err) {
                alert("Lỗi: " + err.responseJSON.error);
            }
        });
    });
    
    // Tải dữ liệu ban đầu
    loadData();
});

// Xóa sinh viên
function deleteStudent(rowid) {
    $.ajax({
        url: `/delete_data/${rowid}`,
        type: "DELETE",
        success: function() {
            alert("Xóa thành công!");
            loadData();  // Cập nhật lại bảng sau khi xóa
        },
        error: function(err) {
            alert("Lỗi: " + err.responseJSON.error);
        }
    });
}
