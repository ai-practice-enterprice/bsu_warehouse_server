<?php
    if (!defined("APP_STARTED")) {
        header("Location: ../bsu.php");
    }

    if (true) {
        header("Location: ../bsu.php");
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>bsu : mailbox</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/bsu_general_style.css">
    <link rel="icon" type="image/x-icon" href="../assets/bsu_ai_icon.svg">
</head>
<body>
    <div class="card" id="mailbox-container">
        <!-- Will be populated with API -->
        <!-- div class="card" * nbr_of_mails -->
    </div>
</body>
</html>