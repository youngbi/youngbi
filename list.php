<?php
session_start();

// Bật chế độ debug để xem lỗi chi tiết
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Kiểm tra và bao gồm autoload của thư viện PHPePub
if (!file_exists('vendor/autoload.php')) {
    die("Lỗi: Không tìm thấy vendor/autoload.php. Vui lòng chạy composer install để cài đặt thư viện PHPePub.");
}
require_once 'vendor/autoload.php';

function sanitizeFolderName($name) {
    return preg_replace('/[^a-zA-Z0-9-_]/', '-', strtolower(trim($name)));
}

$translatedDir = 'translated/';
$stories = [];

// Kiểm tra thư mục translated/ có tồn tại và có quyền truy cập không
if (!is_dir($translatedDir) || !is_readable($translatedDir)) {
    die("Lỗi: Thư mục $translatedDir không tồn tại hoặc không có quyền truy cập.");
}

foreach (scandir($translatedDir) as $folder) {
    if ($folder === '.' || $folder === '..') continue;

    $epubFiles = glob("$translatedDir$folder/*.epub");
    if (!empty($epubFiles)) {
        try {
            // Khởi tạo đối tượng EPUB để lấy tiêu đề gốc
            $book = new PHPePub\Core\EPub($epubFiles[0]);
            $originalTitle = $book->getTitle() ?: ucwords(str_replace('-', ' ', $folder));

            $chaptersDir = "chapters/$folder/";
            $translatedChaptersDir = "translated_chapters/$folder/";
            $chapterCount = 0;
            $totalChapters = 0;

            // Kiểm tra và đếm số chương gốc
            if (is_dir($chaptersDir) && is_readable($chaptersDir)) {
                $originalChapters = glob("$chaptersDir*.txt");
                $totalChapters = count($originalChapters);
            } else {
                file_put_contents('debug.log', "Cảnh báo: Thư mục $chaptersDir không tồn tại hoặc không có quyền truy cập.\n", FILE_APPEND);
            }

            // Kiểm tra và đếm số chương đã dịch
            if (is_dir($translatedChaptersDir) && is_readable($translatedChaptersDir)) {
                $translatedChapters = glob("$translatedChaptersDir*.txt");
                $chapterCount = count($translatedChapters);
            } else {
                file_put_contents('debug.log', "Cảnh báo: Thư mục $translatedChaptersDir không tồn tại hoặc không có quyền truy cập.\n", FILE_APPEND);
            }

            $stories[] = [
                'originalTitle' => $originalTitle,
                'translatedTitle' => ucwords(str_replace('-', ' ', $folder)),
                'file' => $epubFiles[0],
                'chapterCount' => $chapterCount,
                'totalChapters' => $totalChapters
            ];
        } catch (Exception $e) {
            file_put_contents('debug.log', "Lỗi khi đọc file EPUB $epubFiles[0]: " . $e->getMessage() . "\n", FILE_APPEND);
        }
    }
}

$perPage = 10;
$totalStories = count($stories);
$totalPages = ceil($totalStories / $perPage);
$page = isset($_GET['page']) ? max(1, min((int)$_GET['page'], $totalPages)) : 1;
$start = ($page - 1) * $perPage;
$currentStories = array_slice($stories, $start, $perPage);
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Danh Sách Truyện Đã Dịch</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .btn {
            padding: 5px 10px;
            background-color: #8a4af3;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .btn:hover {
            background-color: #6d2dc6;
        }
        .disabled {
            background-color: #ccc;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Danh Sách Truyện Đã Dịch</h1>
        <?php if (empty($stories)): ?>
            <p>Chưa có truyện nào được dịch.</p>
        <?php else: ?>
            <table>
                <thead>
                    <tr>
                        <th>Tên Truyện</th>
                        <th>Số Chương Đã Dịch / Tổng Số Chương</th>
                        <th>Tải Về</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($currentStories as $story): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($story['originalTitle']); ?></td>
                            <td><?php echo htmlspecialchars("{$story['chapterCount']} / {$story['totalChapters']}"); ?></td>
                            <td style="text-align: center;">
                                <a href="download.php?file=<?php echo urlencode($story['file']); ?>" class="btn">Tải EPUB</a>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>

            <!-- Phân trang -->
            <div style="text-align: center;">
                <?php if ($page > 1): ?>
                    <a href="?page=<?php echo $page - 1; ?>" class="btn">Trang trước</a>
                <?php endif; ?>
                <?php for ($i = 1; $i <= $totalPages; $i++): ?>
                    <a href="?page=<?php echo $i; ?>" class="btn <?php echo $i === $page ? 'disabled' : ''; ?>"><?php echo $i; ?></a>
                <?php endfor; ?>
                <?php if ($page < $totalPages): ?>
                    <a href="?page=<?php echo $page + 1; ?>" class="btn">Trang sau</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>

        <a href="index.html" class="btn" style="margin-top: 20px;">Quay lại dịch truyện</a>
    </div>
</body>
</html>