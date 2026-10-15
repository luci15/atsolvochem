<?php
// Enquiry form handler for contact.html. Redirects back with ?sent=1 (ok) or ?sent=0 (failed).

$to   = "prashantjagadale@gmail.com";
$from = "sales@atsolvochem.com";

function clean($v, $max)
{
    $v = isset($v) ? trim((string) $v) : '';
    $v = str_replace(array("\r", "\n", "%0a", "%0d"), ' ', $v); // block header injection
    return mb_substr($v, 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: contact.html');
    exit;
}

// honeypot: bots fill this hidden field
if (!empty($_POST['website'])) {
    header('Location: contact.html?sent=1');
    exit;
}

$name  = clean($_POST['userName'] ?? '', 120);
$email = clean($_POST['userEmail'] ?? '', 160);
$phone = clean($_POST['userPhone'] ?? '', 40);
$msg   = mb_substr(trim((string) ($_POST['userMsg'] ?? '')), 0, 4000);

if ($name === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: contact.html?sent=0');
    exit;
}

$subject = "Website enquiry from $name";
$body    = "Name: $name\nEmail: $email\nMobile: $phone\n\nEnquiry:\n$msg\n";
$headers = "From: A T Solvochem Website <$from>\r\n"
         . "Reply-To: $email\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";

$sent = mail($to, $subject, $body, $headers);
header('Location: contact.html?sent=' . ($sent ? '1' : '0'));
exit;
