<?php
session_start();

require_once 'vendor/autoload.php';

use PHPePub\Core\EPub;

header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
header('Connection: keep-alive');

// Tăng thời gian thực thi tối đa lên 300 giây (5 phút)
ini_set('max_execution_time', 300);

function sendEvent($event, $data) {
    echo "event: $event\n";
    echo "data: " . json_encode($data, JSON_UNESCAPED_UNICODE) . "\n\n";
    @ob_flush();
    flush();
}

function sanitizeFolderName($name) {
    return preg_replace('/[^a-zA-Z0-9-_]/', '-', strtolower(trim($name)));
}

function isTableOfContents($filePath) {
    $doc = new DOMDocument();
    @$doc->loadHTMLFile($filePath, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
    $xpath = new DOMXPath($doc);

    $linkNodes = $xpath->query('//a');
    $listNodes = $xpath->query('//li');
    $totalLinksOrItems = $linkNodes->length + $listNodes->length;

    $threshold = 5;
    if ($totalLinksOrItems < $threshold) {
        return false;
    }

    $titleNodes = $xpath->query('//title | //h1');
    foreach ($titleNodes as $node) {
        $titleText = trim($node->nodeValue);
        if (preg_match('/\d/', $titleText)) {
            return false;
        }
    }

    return true;
}

function isIntroduction($filePath, $chapterTitle) {
    $doc = new DOMDocument();
    @$doc->loadHTMLFile($filePath, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
    $xpath = new DOMXPath($doc);

    $titleNodes = $xpath->query('//title | //h1');
    foreach ($titleNodes as $node) {
        $titleText = trim($node->nodeValue);
        $introKeywords = ['giới thiệu', 'lời mở đầu', 'mở đầu', 'prologue', '前言', '引言'];
        $titleLower = mb_strtolower($titleText, 'UTF-8');
        $hasKeyword = false;
        foreach ($introKeywords as $keyword) {
            if (mb_strpos($titleLower, $keyword, 0, 'UTF-8') !== false) {
                $hasKeyword = true;
                break;
            }
        }
        if (!preg_match('/\d/', $titleText) || $hasKeyword) {
            return true;
        }
    }
    $chapterTitleLower = mb_strtolower($chapterTitle, 'UTF-8');
    foreach ($introKeywords as $keyword) {
        if (mb_strpos($chapterTitleLower, $keyword, 0, 'UTF-8') !== false) {
            return true;
        }
    }
    return false;
}

function getContentChapterIndex($chapterFiles, $chapter) {
    $contentIndex = -1;
    for ($i = 0; $i <= $chapter; $i++) {
        if (isset($chapterFiles[$i])) {
            $filePath = $chapterFiles[$i]['file'];
            if (!isTableOfContents($filePath) && !isIntroduction($filePath, $chapterFiles[$i]['title'])) {
                $contentIndex++;
            }
        }
    }
    return max(0, $contentIndex);
}

function translateHtmlContent($apiKey, $prompt, $htmlContent, $chapterIndex, &$mh, &$chHandles) {
    $doc = new DOMDocument();
    @$doc->loadHTML($htmlContent, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
    $xpath = new DOMXPath($doc);

    $originalTitle = '';
    $titleNodes = $xpath->query('//title');
    if ($titleNodes->length > 0) {
        $originalTitle = trim($titleNodes->item(0)->nodeValue);
    }

    $chapterNumberPrefix = '';
    $chapterTitleText = '';
    $h1Nodes = $xpath->query('//h1');
    if ($h1Nodes->length > 0) {
        $h1Text = trim($h1Nodes->item(0)->nodeValue);
        if (preg_match('/^(\d+\.)(.+)$/', $h1Text, $matches)) {
            $chapterNumberPrefix = $matches[1];
            $chapterTitleText = trim($matches[2]);
        } else {
            $chapterTitleText = $h1Text;
        }
    }

    $bodyText = $chapterTitleText . "\n";
    $bodyNodes = $xpath->query('//body//p//text()[normalize-space(.) != ""]');
    foreach ($bodyNodes as $node) {
        $text = trim($node->nodeValue);
        if ($text) {
            $bodyText .= $text . "\n";
        }
    }
    $bodyText = trim($bodyText);

    if (empty($bodyText)) {
        return [
            'doc' => $doc,
            'originalTitle' => $originalTitle,
            'chapterNumberPrefix' => $chapterNumberPrefix,
            'chapterTitleText' => $chapterTitleText
        ];
    }

    $apiUrl = "https://api.x.ai/v1/chat/completions";
    $payload = [
        'model' => 'grok-2-1212',
        'messages' => [
            ['role' => 'system', 'content' => $prompt . "\nDịch toàn bộ nội dung dưới đây. Lưu ý dòng đầu tiên là tiêu đề chương, hãy dịch nhưng không thêm ký tự như ### hay bất kỳ định dạng Markdown nào."],
            ['role' => 'user', 'content' => $bodyText]
        ],
        'max_tokens' => 8192,
        'temperature' => 0.7
    ];

    $ch = curl_init($apiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $apiKey
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_TIMEOUT, 180);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);

    $chHandles[$chapterIndex] = $ch;
    curl_multi_add_handle($mh, $ch);

    return [
        'doc' => $doc,
        'originalTitle' => $originalTitle,
        'chapterNumberPrefix' => $chapterNumberPrefix,
        'chapterTitleText' => $chapterTitleText
    ];
}

function syncChapterTitlesWithTOC($chapterFiles, &$translatedChapters, $tocChapterIndex, $translatedDir) {
    $tocFilePath = $chapterFiles[$tocChapterIndex]['file'];
    $doc = new DOMDocument();
    @$doc->loadHTMLFile($tocFilePath, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
    $xpath = new DOMXPath($doc);

    $linkNodes = $xpath->query('//a');
    $chapterTitlesFromTOC = [];
    foreach ($linkNodes as $node) {
        $href = $node->getAttribute('href');
        $title = trim($node->nodeValue);
        $chapterTitlesFromTOC[$href] = $title;
    }

    foreach ($translatedChapters as $chapter => &$chapterData) {
        if (isset($chapterFiles[$chapter]) && $chapter != $tocChapterIndex) {
            $relativePath = $chapterFiles[$chapter]['relativePath'];
            if (isset($chapterTitlesFromTOC[$relativePath])) {
                $newTitle = $chapterTitlesFromTOC[$relativePath];
                $translatedFile = $chapterData['file'];
                $chapterDoc = new DOMDocument();
                @$chapterDoc->loadHTMLFile($translatedFile, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
                $chapterXpath = new DOMXPath($chapterDoc);

                $titleNodes = $chapterXpath->query('//title');
                if ($titleNodes->length > 0) {
                    $titleNodes->item(0)->nodeValue = $newTitle;
                }

                $h1Nodes = $chapterXpath->query('//h1');
                if ($h1Nodes->length > 0) {
                    $h1Nodes->item(0)->nodeValue = $newTitle;
                }

                $updatedContent = '<?xml version="1.0" encoding="utf-8"?>' . "\n" .
                    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' . "\n" .
                    $chapterDoc->saveXML($chapterDoc->documentElement);
                file_put_contents($translatedFile, $updatedContent, LOCK_EX);

                $chapterData['title'] = $newTitle;
            }
        }
    }
}

function syncChapterTitlesWithNCX($chapterFiles, &$translatedChapters, $extractDir) {
    $ncxFile = glob($extractDir . '*/toc.ncx')[0] ?? '';
    if (!$ncxFile || !file_exists($ncxFile)) {
        return;
    }

    $doc = new DOMDocument();
    @$doc->load($ncxFile);
    $xpath = new DOMXPath($doc);
    $xpath->registerNamespace('ncx', 'http://www.daisy.org/z3986/2005/ncx/');

    $navPoints = $xpath->query('//ncx:navPoint');
    $chapterTitlesFromNCX = [];
    foreach ($navPoints as $navPoint) {
        $navLabel = $xpath->query('ncx:navLabel/ncx:text', $navPoint)->item(0);
        $contentSrc = $xpath->query('ncx:content/@src', $navPoint)->item(0);
        if ($navLabel && $contentSrc) {
            $href = $contentSrc->nodeValue;
            $title = trim($navLabel->nodeValue);
            $chapterTitlesFromNCX[$href] = $title;
        }
    }

    foreach ($translatedChapters as $chapter => &$chapterData) {
        if (isset($chapterFiles[$chapter])) {
            $relativePath = $chapterFiles[$chapter]['relativePath'];
            if (isset($chapterTitlesFromNCX[$relativePath])) {
                $newTitle = $chapterTitlesFromNCX[$relativePath];
                $translatedFile = $chapterData['file'];
                $chapterDoc = new DOMDocument();
                @$chapterDoc->loadHTMLFile($translatedFile, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
                $chapterXpath = new DOMXPath($chapterDoc);

                $titleNodes = $chapterXpath->query('//title');
                if ($titleNodes->length > 0) {
                    $titleNodes->item(0)->nodeValue = $newTitle;
                }

                $h1Nodes = $chapterXpath->query('//h1');
                if ($h1Nodes->length > 0) {
                    $h1Nodes->item(0)->nodeValue = $newTitle;
                }

                $updatedContent = '<?xml version="1.0" encoding="utf-8"?>' . "\n" .
                    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' . "\n" .
                    $chapterDoc->saveXML($chapterDoc->documentElement);
                file_put_contents($translatedFile, $updatedContent, LOCK_EX);

                $chapterData['title'] = $newTitle;
            }
        }
    }
}

function updateEpubMetadata($chapterFiles, $translatedChapters, $extractDir, $tocChapterIndex) {
    $opfFile = glob($extractDir . '*/content.opf')[0] ?? '';
    if ($opfFile && file_exists($opfFile)) {
        $doc = new DOMDocument();
        @$doc->load($opfFile);
        $xpath = new DOMXPath($doc);
        $xpath->registerNamespace('opf', 'http://www.idpf.org/2007/opf');

        $itemrefs = $xpath->query('//opf:itemref');
        foreach ($itemrefs as $index => $itemref) {
            if (isset($chapterFiles[$index]) && isset($translatedChapters[$index])) {
                $idref = $itemref->getAttribute('idref');
                $item = $xpath->query("//opf:item[@id='$idref']")->item(0);
                if ($item) {
                    $href = $item->getAttribute('href');
                    if ($href === $chapterFiles[$index]['relativePath']) {
                        $newTitle = $translatedChapters[$index]['title'];
                        if (!isIntroduction($chapterFiles[$index]['file'], $chapterFiles[$index]['title']) && $index != $tocChapterIndex) {
                            $newTitle = "Chương " . (getContentChapterIndex($chapterFiles, $index) + 1);
                        }
                        $manifestItem = $xpath->query("//opf:manifest/opf:item[@id='$idref']")->item(0);
                        if ($manifestItem) {
                            $manifestItem->setAttribute('properties', 'nav');
                        }
                    }
                }
            }
        }

        $metadata = $xpath->query('//opf:metadata')->item(0);
        if ($metadata) {
            $title = $xpath->query('dc:title', $metadata)->item(0);
            if ($title) {
                $title->nodeValue = $_SESSION['storyTitle'] ?? 'Unknown Title';
            }
        }

        file_put_contents($opfFile, $doc->saveXML());
    }

    $ncxFile = glob($extractDir . '*/toc.ncx')[0] ?? '';
    if ($ncxFile && file_exists($ncxFile)) {
        $doc = new DOMDocument();
        @$doc->load($ncxFile);
        $xpath = new DOMXPath($doc);
        $xpath->registerNamespace('ncx', 'http://www.daisy.org/z3986/2005/ncx/');

        $navPoints = $xpath->query('//ncx:navPoint');
        foreach ($navPoints as $index => $navPoint) {
            if (isset($chapterFiles[$index]) && isset($translatedChapters[$index])) {
                $navLabel = $xpath->query('ncx:navLabel/ncx:text', $navPoint)->item(0);
                if ($navLabel) {
                    $newTitle = $translatedChapters[$index]['title'];
                    if (!isIntroduction($chapterFiles[$index]['file'], $chapterFiles[$index]['title']) && $index != $tocChapterIndex) {
                        $newTitle = "Chương " . (getContentChapterIndex($chapterFiles, $index) + 1);
                    }
                    $navLabel->nodeValue = $newTitle;
                }
            }
        }

        file_put_contents($ncxFile, $doc->saveXML());
    }
}

$stateFile = 'translation_state.json';

ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', 'php_errors.log');

$apiKeys = isset($_GET['apiKeys']) ? array_filter(explode("\n", trim($_GET['apiKeys']))) : [];
$prompt = $_GET['prompt'] ?? '';
$startChapter = isset($_GET['startChapter']) ? (int)$_GET['startChapter'] : 0;
$endChapter = isset($_GET['endChapter']) ? (int)$_GET['endChapter'] : 0;

if (empty($apiKeys)) {
    sendEvent('error', ['message' => 'API key không được để trống!']);
    exit;
}
if (!$prompt) {
    sendEvent('error', ['message' => 'Lệnh dịch không được để trống!']);
    exit;
}
if (!isset($_SESSION['chapterFiles']) || empty($_SESSION['chapterFiles'])) {
    sendEvent('error', ['message' => 'Không tìm thấy danh sách chương! Vui lòng tải lên file EPUB trước.']);
    exit;
}

$chapterFiles = $_SESSION['chapterFiles'];
$totalChapters = count($chapterFiles);
$storyFolder = sanitizeFolderName($_SESSION['storyTitle'] ?? 'unknown');
$extractDir = $_SESSION['extractDir'];

$contentChapterCount = 0;
$chapterMap = [];
for ($i = 0; $i < $totalChapters; $i++) {
    $filePath = $chapterFiles[$i]['file'];
    if (!isTableOfContents($filePath) && !isIntroduction($filePath, $chapterFiles[$i]['title'])) {
        $chapterMap[$i] = $contentChapterCount;
        $contentChapterCount++;
    } else {
        $chapterMap[$i] = -1;
    }
}

$totalContentChapters = $contentChapterCount;
if ($startChapter < 1 || $endChapter < $startChapter || $endChapter > $totalContentChapters) {
    sendEvent('error', ["message" => "Khoảng chương không hợp lệ! Tổng số chương nội dung: $totalContentChapters"]);
    exit;
}

$actualStartChapter = array_search($startChapter - 1, array_values($chapterMap), true);
$actualEndChapter = array_search($endChapter - 1, array_values($chapterMap), true);

if ($actualStartChapter === false || $actualEndChapter === false) {
    sendEvent('error', ["message" => "Khoảng chương nội dung chính không hợp lệ!"]);
    exit;
}

$translatedDir = "translated_chapters/$storyFolder/";
if (!is_dir($translatedDir)) {
    mkdir($translatedDir, 0777, true) or file_put_contents('debug.log', "Cannot create directory $translatedDir\n", FILE_APPEND);
}

$state = file_exists($stateFile) && ($stateData = json_decode(file_get_contents($stateFile), true)) ? $stateData : [
    'progress' => 0,
    'translatedChapters' => [],
    'errors' => [],
    'log' => "Log Tiến Trình:\n",
    'tocChapters' => [],
    'introChapters' => []
];

$translatedChapters = $state['translatedChapters'] ?? [];
$errors = $state['errors'] ?? [];
$tocChapters = $state['tocChapters'] ?? [];
$introChapters = $state['introChapters'] ?? [];

$maxConcurrentChapters = 5;

$chaptersToTranslate = [];
for ($chapter = 0; $chapter < $totalChapters; $chapter++) {
    $filePath = $chapterFiles[$chapter]['file'];
    if (isTableOfContents($filePath)) {
        continue;
    }
    if (!isset($translatedChapters[$chapter]) && ($chapter >= $actualStartChapter && $chapter <= $actualEndChapter || isIntroduction($filePath, $chapterFiles[$chapter]['title']))) {
        $chaptersToTranslate[] = $chapter;
    }
}

$chapterCount = count($chaptersToTranslate);
$apiKeyCount = count($apiKeys);
$apiKeyIndex = 0;

for ($i = 0; $i < $chapterCount; $i += $maxConcurrentChapters) {
    $mh = curl_multi_init();
    $chHandles = [];
    $chapterData = [];
    $currentBatch = array_slice($chaptersToTranslate, $i, $maxConcurrentChapters);

    foreach ($currentBatch as $chapter) {
        if (!isset($chapterFiles[$chapter]) || !file_exists($chapterFiles[$chapter]['file'])) {
            $errors[$chapter] = "Không tìm thấy file chương $chapter!";
            $state['errors'] = $errors;
            $state['log'] .= "Lỗi dịch: Chương " . ($chapterMap[$chapter] + 1) . " - Không tìm thấy file chương $chapter!\n";
            file_put_contents($stateFile, json_encode($state, JSON_UNESCAPED_UNICODE));
            sendEvent('progress', [
                'progress' => $state['progress'],
                'log' => $state['log'],
                'chapter' => $chapterMap[$chapter] + 1,
                'chapterTitle' => $chapterFiles[$chapter]['title'] ?? "Unknown"
            ]);
            continue;
        }

        if (isset($translatedChapters[$chapter])) {
            continue;
        }

        $filePath = $chapterFiles[$chapter]['file'];
        $htmlContent = file_get_contents($filePath);
        $apiKey = $apiKeys[$apiKeyIndex % $apiKeyCount];
        $apiKeyIndex++;
        $chapterData[$chapter] = translateHtmlContent($apiKey, $prompt, $htmlContent, $chapter, $mh, $chHandles);
        if (isIntroduction($filePath, $chapterFiles[$chapter]['title'])) {
            $introChapters[$chapter] = true;
            $state['introChapters'] = $introChapters;
        }
    }

    do {
        curl_multi_exec($mh, $running);
        curl_multi_select($mh);

        while ($info = curl_multi_info_read($mh)) {
            $ch = $info['handle'];
            foreach ($chHandles as $chapter => $handle) {
                if ($handle === $ch) {
                    $response = curl_multi_getcontent($ch);
                    if ($response && !curl_errno($ch)) {
                        $result = json_decode($response, true);
                        if ($result && isset($result['choices'][0]['message']['content'])) {
                            $translatedText = $result['choices'][0]['message']['content'];
                            $translatedLines = array_filter(array_map('trim', explode("\n", $translatedText)));
                            $doc = $chapterData[$chapter]['doc'];
                            $originalTitle = $chapterData[$chapter]['originalTitle'];
                            $chapterNumberPrefix = $chapterData[$chapter]['chapterNumberPrefix'];
                            $chapterTitleText = $chapterData[$chapter]['chapterTitleText'];
                            $xpath = new DOMXPath($doc);

                            $translatedTitle = !empty($translatedLines) ? array_shift($translatedLines) : $chapterTitleText;
                            if ($chapterNumberPrefix) {
                                $translatedTitle = $chapterNumberPrefix . " " . $translatedTitle;
                            }

                            $titleNodes = $xpath->query('//title');
                            if ($titleNodes->length > 0) {
                                $titleNodes->item(0)->nodeValue = $translatedTitle;
                            }
                            $h1Nodes = $xpath->query('//h1');
                            if ($h1Nodes->length > 0) {
                                $h1Nodes->item(0)->nodeValue = $translatedTitle;
                            }

                            $pNodes = $xpath->query('//p');
                            $contentIndex = 0;
                            foreach ($pNodes as $index => $node) {
                                if (isset($translatedLines[$contentIndex])) {
                                    while ($node->hasChildNodes()) {
                                        $node->removeChild($node->firstChild);
                                    }
                                    $node->appendChild($doc->createTextNode($translatedLines[$contentIndex]));
                                    $contentIndex++;
                                }
                            }

                            $chapterFiles[$chapter]['title'] = $translatedTitle;

                            $translatedContent = '<?xml version="1.0" encoding="utf-8"?>' . "\n" .
                                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' . "\n" .
                                $doc->saveXML($doc->documentElement);
                            $translatedFile = $translatedDir . basename($chapterFiles[$chapter]['relativePath']);
                            file_put_contents($translatedFile, $translatedContent, LOCK_EX);
                            $translatedChapters[$chapter] = [
                                'title' => $translatedTitle,
                                'file' => $translatedFile,
                                'relativePath' => $chapterFiles[$chapter]['relativePath']
                            ];
                        } else {
                            $errors[$chapter] = "Invalid API response: " . substr($response, 0, 500);
                        }
                    } else {
                        $errors[$chapter] = "cURL error: " . curl_error($ch);
                    }
                    curl_multi_remove_handle($mh, $ch);
                    unset($chHandles[$chapter]);
                    unset($chapterData[$chapter]);
                }
            }

            $completedChapters = count(array_filter(array_keys($translatedChapters), function($chapter) use ($chapterMap) {
                return isset($chapterMap[$chapter]) && $chapterMap[$chapter] >= 0 && $chapter >= $actualStartChapter && $chapter <= $actualEndChapter;
            }));
            $errorCount = count(array_filter(array_keys($errors), function($chapter) use ($chapterMap) {
                return isset($chapterMap[$chapter]) && $chapterMap[$chapter] >= 0 && $chapter >= $actualStartChapter && $chapter <= $actualEndChapter;
            }));
            $progress = $chapterCount > 0 ? min(100, (($completedChapters - $errorCount) / $chapterCount) * 100) : 0;
            $state['progress'] = $progress;
            $state['translatedChapters'] = $translatedChapters;
            $state['errors'] = $errors;
            $state['tocChapters'] = $tocChapters;
            $state['introChapters'] = $introChapters;

            $log = "Log Tiến Trình:\n";
            ksort($translatedChapters);
            foreach ($translatedChapters as $chapter => $data) {
                $displayIndex = getContentChapterIndex($chapterFiles, $chapter);
                if (isset($tocChapters[$chapter])) {
                    $log .= "Bỏ qua dịch: Mục Lục - {$data['title']}\n";
                } elseif (isset($introChapters[$chapter])) {
                    $log .= "Đã dịch thành công: Giới Thiệu - {$data['title']}\n";
                } else {
                    $chapterDisplayIndex = $displayIndex + 1;
                    $log .= "Đã dịch thành công: Chương $chapterDisplayIndex - {$data['title']}\n";
                }
            }
            foreach ($errors as $chapter => $error) {
                $displayIndex = getContentChapterIndex($chapterFiles, $chapter);
                if (isset($tocChapters[$chapter])) {
                    $log .= "Lỗi dịch: Mục Lục - $error\n";
                } elseif (isset($introChapters[$chapter])) {
                    $log .= "Lỗi dịch: Giới Thiệu - $error\n";
                } else {
                    $chapterDisplayIndex = $displayIndex + 1;
                    $log .= "Lỗi dịch: Chương $chapterDisplayIndex - $error\n";
                }
            }
            $state['log'] = $log;
            file_put_contents($stateFile, json_encode($state, JSON_UNESCAPED_UNICODE));

            sendEvent('progress', [
                'progress' => $progress,
                'log' => $log
            ]);
        }
    } while ($running > 0);

    curl_multi_close($mh);
}

$tocChapterIndex = null;
for ($chapter = 0; $chapter < $totalChapters; $chapter++) {
    $filePath = $chapterFiles[$chapter]['file'];
    if (isTableOfContents($filePath)) {
        $tocChapterIndex = $chapter;
        $tocChapters[$chapter] = true;
        $state['tocChapters'] = $tocChapters;
        $state['log'] .= "Bỏ qua dịch: Mục Lục - {$chapterFiles[$chapter]['title']}\n";
        break;
    }
}

if ($tocChapterIndex !== null) {
    syncChapterTitlesWithTOC($chapterFiles, $translatedChapters, $tocChapterIndex, $translatedDir);
} else {
    syncChapterTitlesWithNCX($chapterFiles, $translatedChapters, $extractDir);
}

updateEpubMetadata($chapterFiles, $translatedChapters, $extractDir, $tocChapterIndex);

if ($state['progress'] >= 100 && empty($errors)) {
    $translatedRootDir = "translated/$storyFolder/";
    if (!is_dir($translatedRootDir)) {
        mkdir($translatedRootDir, 0777, true);
    }

    $newEpubFile = "$translatedRootDir/translated_" . basename($_SESSION['epubPath'], '.epub') . "_" . time() . '.epub';
    $zip = new ZipArchive();
    if ($zip->open($newEpubFile, ZipArchive::CREATE | ZipArchive::OVERWRITE) !== true) {
        sendEvent('error', ['message' => 'Không thể tạo file EPUB mới!']);
        exit;
    }

    $iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($extractDir));
    foreach ($iterator as $file) {
        if ($file->isDir()) continue;
        $relativePath = substr($file->getPathname(), strlen($extractDir));
        if (!preg_match('/\.(html|xhtml)$/', $relativePath)) {
            $zip->addFile($file->getPathname(), $relativePath);
        }
    }

    for ($chapter = 0; $chapter < $totalChapters; $chapter++) {
        if (isset($chapterFiles[$chapter])) {
            $relativePath = $chapterFiles[$chapter]['relativePath'];
            if (isset($translatedChapters[$chapter])) {
                $zip->addFile($translatedChapters[$chapter]['file'], $relativePath);
            } else {
                $zip->addFile($chapterFiles[$chapter]['file'], $relativePath);
            }
        }
    }

    $zip->close();
    $_SESSION['translatedFile'] = $newEpubFile;

    array_map('unlink', glob("$translatedDir/*"));
    rmdir($translatedDir);

    $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    $domain = $_SERVER['HTTP_HOST'];
    $basePath = rtrim(dirname($_SERVER['SCRIPT_NAME']), '/');
    $downloadUrl = "$protocol://$domain$basePath/translated/$storyFolder/" . basename($newEpubFile);

    sendEvent('complete', [
        'progress' => 100,
        'log' => $state['log'] . "Dịch hoàn tất: $newEpubFile\n",
        'downloadUrl' => $downloadUrl
    ]);

    if (file_exists($stateFile)) {
        unlink($stateFile);
    }
} else {
    sendEvent('complete', [
        'progress' => $state['progress'],
        'log' => $state['log'],
        'errors' => $errors
    ]);
}

exit;
?>