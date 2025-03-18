$(document).ready(function() {
    // Ẩn progress bar ban đầu
    $('.progress-bar').hide();

    // Xử lý sự kiện khi chọn file
    $('#epubUpload').on('change', function(e) {
        const file = e.target.files[0];
        $('#fileName').text(file ? file.name : 'Chưa chọn tệp');
    });

    // Xử lý sự kiện khi nhấn nút "Tải Lên EPUB"
    $('#uploadBtn').on('click', function(e) {
        e.preventDefault();
        const fileInput = $('#epubUpload')[0];
        const file = fileInput.files[0];
        if (!file || !file.name.endsWith('.epub')) {
            $('#uploadError').text('Vui lòng chọn file EPUB!').show();
            return;
        }

        const formData = new FormData();
        formData.append('epubFile', file);
        const storyTitle = $('#storyTitle').val();
        if (storyTitle) {
            formData.append('storyTitle', storyTitle);
        }

        $('#uploadError').hide();
        $('.progress-bar').eq(0).show(); // Hiển thị progress bar đầu tiên (upload)
        $('#progress').eq(0).css('width', '0%').text('Đang tải lên: 0%');
        $('#uploadBtn').prop('disabled', true);

        $.ajax({
            url: 'upload.php',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            xhr: function() {
                const xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function(evt) {
                    if (evt.lengthComputable) {
                        const percent = (evt.loaded / evt.total) * 100;
                        $('#progress').eq(0).css('width', percent + '%')
                                           .text(`Đang tải lên: ${percent.toFixed(2)}%`);
                    }
                }, false);
                return xhr;
            },
            success: function(response) {
                $('#uploadBtn').prop('disabled', false);
                if (response.success) {
                    $('#progress').eq(0).css('width', '100%').text('Tải lên hoàn tất: 100%');
                    $('#storyInfo').show();
                    $('#storyTitle').text(response.title);
                    $('#storyAuthor').text(response.author);
                    $('#totalChapters').text(response.totalChapters);
                    $('#chapterList').empty();
                    response.chapters.forEach(chapter => {
                        $('#chapterList').append(`<li>${chapter}</li>`);
                    });
                    $('#startChapter').val(1);
                    $('#endChapter').val(response.totalChapters - 1);
                    $('#translateSection').show();
                    setTimeout(() => $('.progress-bar').eq(0).hide(), 1000);
                } else {
                    $('#progress').eq(0).css('width', '0%').text('Lỗi: ' + (response.error || 'Không xác định'));
                    $('#uploadError').text(response.error || 'Lỗi không xác định khi tải lên!').show();
                    $('.progress-bar').eq(0).hide();
                }
            },
            error: function(xhr, status, error) {
                $('#uploadBtn').prop('disabled', false);
                $('#progress').eq(0).css('width', '0%').text('Lỗi kết nối!');
                $('#uploadError').text(`Lỗi kết nối khi tải lên! Chi tiết: ${status} - ${error}`).show();
                $('.progress-bar').eq(0).hide();
            }
        });
    });

    // Ẩn các phần không cần thiết ban đầu
    $('#storyInfo, #translateSection').hide();
});

function translateStory() {
    const apiKeys = $('#apiKeys').val().trim();
    const prompt = $('#promptInput').val();
    const startChapter = parseInt($('#startChapter').val());
    const endChapter = parseInt($('#endChapter').val());
    const totalChapters = parseInt($('#totalChapters').text());

    if (!apiKeys) {
        $('#translateError').text('Vui lòng nhập ít nhất một API key!').show();
        return;
    }
    if (!prompt) {
        $('#translateError').text('Vui lòng nhập lệnh dịch!').show();
        return;
    }
    if (isNaN(startChapter) || startChapter < 1) {
        $('#translateError').text('Chương bắt đầu không hợp lệ! Phải lớn hơn hoặc bằng 1.').show();
        return;
    }
    if (isNaN(endChapter) || endChapter < 1 || endChapter >= totalChapters || startChapter > endChapter) {
        $('#translateError').text('Chương kết thúc không hợp lệ!').show();
        return;
    }

    $('#translateError').hide();
    $('#downloadBtn').prop('disabled', true);
    $('.progress-bar').eq(1).show(); // Hiển thị progress bar thứ hai (dịch)
    $('#progress').eq(1).css('width', '0%').text('Đang dịch: 0%');
    $('#logOutput').val('Log Tiến Trình:\n');

    const url = `translate.php?apiKeys=${encodeURIComponent(apiKeys)}&prompt=${encodeURIComponent(prompt)}&startChapter=${startChapter}&endChapter=${endChapter}`;
    const source = new EventSource(url, { withCredentials: true });

    source.addEventListener('progress', function(event) {
        const data = JSON.parse(event.data);
        $('#progress').eq(1).css('width', data.progress + '%').text(`Đang dịch: ${data.progress.toFixed(2)}%`);
        $('#logOutput').val(data.log);
    });

    source.addEventListener('complete', function(event) {
        const data = JSON.parse(event.data);
        $('#progress').eq(1).css('width', data.progress + '%').text(data.progress === 100 ? 'Dịch hoàn tất: 100%' : `Dịch hoàn tất: ${data.progress.toFixed(2)}%`);
        $('#logOutput').val(data.log);
        if (data.progress === 100 && data.downloadUrl) {
            $('#downloadBtn').prop('disabled', false);
            $('#downloadBtn').off('click').on('click', function() {
                window.location.href = data.downloadUrl + '?t=' + new Date().getTime();
            });
        }
        source.close();
        $('.progress-bar').eq(1).hide();
    });

    source.addEventListener('error', function(event) {
        const data = JSON.parse(event.data || '{"message": "Lỗi không xác định"}');
        $('#progress').eq(1).css('width', '0%').text('Lỗi: ' + data.message);
        $('#translateError').text(data.message).show();
        source.close();
        $('.progress-bar').eq(1).hide();
    });

    source.onerror = function() {
        $('#progress').eq(1).css('width', '0%').text('Lỗi kết nối!');
        $('#translateError').text('Mất kết nối với máy chủ!').show();
        source.close();
        $('.progress-bar').eq(1).hide();
    };
}

function downloadEpub() {
    // Hàm này sẽ được gọi khi nút "Tải EPUB" được kích hoạt từ translateStory
}