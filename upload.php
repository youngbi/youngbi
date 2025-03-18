<?php
session_start();

require_once 'vendor/autoload.php';

use PHPePub\Core\EPub;

function sendJsonResponse($success, $error = null, $data = []) {
    header('Content-Type: application/json');
    $response = ['success' => $success];
    if ($error !== null) {
        $response['error'] = $error;
    }
    if (!empty($data)) {
        $response = array_merge($response, $data);
    }
    file_put_contents('debug.log', "Upload response: " . json_encode($response) . "\n", FILE_APPEND);
    echo json_encode($response);
    exit;
}

function sanitizeFolderName($name) {
    return preg_replace('/[^a-zA-Z0-9-_]/', '-', strtolower(trim($name)));
}

// Hàm xử lý file mục lục (giữ nguyên nội dung, không thay đổi tên chương)
function processTableOfContents($filePath) {
    $doc = new DOMDocument();
    @$doc->loadHTMLFile($filePath, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
    $xpath = new DOMXPath($doc);

    // Kiểm tra xem có phải file mục lục không
    $h1Nodes = $xpath->query('//h1[text()="Mục lục"]');
    if ($h1Nodes->length === 0) {
        return false; // Không phải file mục lục
    }

    return true; // Xác nhận là file mục lục nhưng không thay đổi nội dung
}

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !isset($_FILES['epubFile'])) {
    sendJsonResponse(false, 'Yêu cầu không hợp lệ hoặc không có tệp được tải lên!');
}

$file = $_FILES['epubFile'];
$uploadDir = 'uploads/';
if (!is_dir($uploadDir)) {
    if (!mkdir($uploadDir, 0777, true)) {
        sendJsonResponse(false, 'Không thể tạo thư mục uploads!');
    }
}

$filePath = $uploadDir . basename($file['name']);
$allowedTypes = ['application/epub+zip'];
if (!in_array($file['type'], $allowedTypes)) {
    sendJsonResponse(false, 'Tệp không phải định dạng EPUB hợp lệ!');
}

if ($file['size'] > 10 * 1024 * 1024) {
    sendJsonResponse(false, 'Tệp quá lớn! Giới hạn là 10MB.');
}

if (!move_uploaded_file($file['tmp_name'], $filePath)) {
    sendJsonResponse(false, 'Lỗi khi tải tệp lên máy chủ! Kiểm tra quyền thư mục uploads/.');
}

try {
    $book = new EPub($filePath);
    $title = mb_convert_encoding($book->getTitle() ?: '', 'UTF-8', 'auto');
    $author = mb_convert_encoding($book->getAuthor() ?: 'Không rõ tác giả', 'UTF-8', 'auto');

    $zip = new ZipArchive();
    if ($zip->open($filePath) !== true) {
        sendJsonResponse(false, 'Không thể mở file EPUB!');
    }

    $container = $zip->getFromName('META-INF/container.xml');
    if ($container === false) {
        $zip->close();
        sendJsonResponse(false, 'Không tìm thấy file container.xml trong EPUB!');
    }

    preg_match('/full-path="([^"]+)"/', $container, $matches);
    if (!isset($matches[1])) {
        $zip->close();
        sendJsonResponse(false, 'Không tìm thấy đường dẫn OPF trong container.xml!');
    }

    $opfPath = $matches[1];
    $opfContent = $zip->getFromName($opfPath);
    if ($opfContent === false) {
        $zip->close();
        sendJsonResponse(false, 'Không tìm thấy file OPF!');
    }

    $opfXml = simplexml_load_string($opfContent);
    if ($opfXml === false) {
        $zip->close();
        sendJsonResponse(false, 'Không thể phân tích file OPF!');
    }

    $manifest = [];
    foreach ($opfXml->manifest->item as $item) {
        $manifest[(string)$item['id']] = (string)$item['href'];
    }

    $opfDir = dirname($opfPath) === '.' ? '' : dirname($opfPath) . '/';
    $chapterFiles = [];
    $i = 0;

    $storyFolder = sanitizeFolderName($title ?: 'unknown_story_' . time());
    $extractDir = "extracted/$storyFolder/";
    if (!is_dir($extractDir)) {
        mkdir($extractDir, 0777, true);
    }
    $zip->extractTo($extractDir);
    $zip->close();

    foreach ($opfXml->spine->itemref as $itemref) {
        $itemId = (string)$itemref['idref'];
        if (isset($manifest[$itemId])) {
            $chapterPath = $opfDir . $manifest[$itemId];
            $chapterFullPath = $extractDir . $chapterPath;
            if (file_exists($chapterFullPath) && preg_match('/\.(html|xhtml)$/', $chapterPath)) {
                $doc = new DOMDocument();
                @$doc->loadHTMLFile($chapterFullPath, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);

                // Kiểm tra và xử lý file mục lục
                if (processTableOfContents($chapterFullPath)) {
                    $chapterTitle = "Mục lục";
                } else {
                    $chapterTitle = "Chương $i";
                    $h1s = $doc->getElementsByTagName('h1');
                    if ($h1s->length > 0) {
                        $chapterTitle = trim($h1s->item(0)->textContent);
                    }
                    if ($i === 0 && !$title) {
                        $title = $chapterTitle;
                    }
                }

                $chapterFiles[$i] = [
                    'title' => $chapterTitle,
                    'file' => $chapterFullPath,
                    'relativePath' => $chapterPath
                ];
                $i++;
            }
        }
    }

    if (empty($chapterFiles)) {
        sendJsonResponse(false, 'Không tìm thấy chương nào trong file EPUB!');
    }

    $_SESSION['storyTitle'] = $title ?: 'Giới thiệu';
    $_SESSION['storyAuthor'] = $author;
    $_SESSION['epubPath'] = $filePath;
    $_SESSION['extractDir'] = $extractDir;
    $_SESSION['chapterFiles'] = $chapterFiles;
    $_SESSION['totalChapters'] = count($chapterFiles);

    $chapterTitles = array_map(function($chapter) {
        return $chapter['title'];
    }, $chapterFiles);

    file_put_contents('debug.log', "File uploaded: $filePath, Extracted to: $extractDir, Title: $title, Author: $author\n", FILE_APPEND);
    sendJsonResponse(true, null, [
        'title' => $title ?: 'Giới thiệu',
        'author' => $author,
        'totalChapters' => count($chapterFiles),
        'chapters' => $chapterTitles
    ]);
} catch (Exception $e) {
    file_put_contents('debug.log', "Upload error: " . $e->getMessage() . "\n", FILE_APPEND);
    sendJsonResponse(false, 'Lỗi đọc file EPUB: ' . $e->getMessage());
}
?>