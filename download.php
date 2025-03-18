<?php
session_start();

// Đảm bảo không có đầu ra thừa trước khi gửi header
ob_start();

if (!isset($_GET['file']) || !file_exists($_GET['file'])) {
    file_put_contents('debug.log', "Download error: File not specified or does not exist: " . ($_GET['file'] ?? 'null') . "\n", FILE_APPEND);
    die("Tệp không tồn tại!");
}

$file = $_GET['file'];

if (!file_exists($file)) {
    file_put_contents('debug.log', "Download error: File does not exist on disk: $file\n", FILE_APPEND);
    file_put_contents('debug.log', "File path checked: " . realpath($file) . "\n", FILE_APPEND);
    die("Tệp dịch không tồn tại trên ổ đĩa! Vui lòng kiểm tra lại.");
}

// Kiểm tra quyền đọc file
if (!is_readable($file)) {
    file_put_contents('debug.log', "Download error: File not readable: $file. Permissions: " . substr(sprintf('%o', fileperms($file)), -4) . "\n", FILE_APPEND);
    die("Không thể đọc tệp dịch! Vui lòng kiểm tra quyền truy cập.");
}

// Gửi header để trình duyệt hiển thị cửa sổ tải file
header('Content-Description: File Transfer');
header('Content-Type: application/epub+zip');
header('Content-Disposition: attachment; filename="' . basename($file) . '"');
header('Content-Length: ' . filesize($file));
header('Cache-Control: no-cache, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

// Xóa bộ đệm đầu ra để tránh lỗi
ob_end_clean();

// Đọc và gửi file, xử lý lỗi
if (readfile($file) === false) {
    file_put_contents('debug.log', "Download error: Failed to read file: $file\n", FILE_APPEND);
    die("Không thể gửi tệp dịch! Vui lòng kiểm tra file.");
}

// Không xóa file sau khi tải (giữ lại file)
exit;