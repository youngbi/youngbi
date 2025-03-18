<?php
session_start();

function sanitizeFolderName($name) {
    return preg_replace('/[^a-zA-Z0-9-_]/', '-', strtolower(trim($name)));
}

$stateFile = 'translation_state.json';
$debugLogFile = 'debug.log';
$phpErrorsLogFile = 'php_errors.log';

if (isset($_SESSION['epubPath'])) {
    @unlink($_SESSION['epubPath']);
}
if (isset($_SESSION['storyTitle'])) {
    $storyFolder = sanitizeFolderName($_SESSION['storyTitle']);
    array_map('unlink', glob("chapters/$storyFolder/*.txt"));
    array_map('unlink', glob("translated_chapters/$storyFolder/*.txt"));
}

// Xóa translation_state.json khi thoát phiên
if (file_exists($stateFile)) {
    unlink($stateFile);
    file_put_contents('debug.log', "Deleted $stateFile on logout.\n", FILE_APPEND); // Ghi log trước khi xóa debug.log
}

// Xóa debug.log
if (file_exists($debugLogFile)) {
    unlink($debugLogFile);
    file_put_contents('php_errors.log', "Deleted $debugLogFile on logout.\n", FILE_APPEND); // Ghi log trước khi xóa php_errors.log
}

// Xóa php_errors.log
if (file_exists($phpErrorsLogFile)) {
    unlink($phpErrorsLogFile);
}

session_destroy();
header('Location: index.html');
exit;