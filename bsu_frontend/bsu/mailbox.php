<?php
    if (!defined("APP_STARTED")) {
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
    <link rel="stylesheet" href="../css/mailbox.css">
    <link rel="icon" type="image/x-icon" href="../assets/svg/bsu_ai_icon.svg">
</head>
<body>
    <?php Navigation::write_navigation("Mailbox"); ?>

    <div class="container">
        <div class="row mt-4">
            <div class="col-12">
                <h1 class="mb-4">Robot Notifications</h1>
                <div class="alert alert-info mb-4">
                    <strong>Info:</strong> Real-time robot notifications will appear below as they are received.
                </div>
            </div>
        </div>
        
        <div class="card" id="mailbox-container">
            <!-- Will be populated with real-time notifications via SSE -->
            <div class="text-center p-5 text-muted">
                <p>Waiting for robot notifications...</p>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="../javascript/general_config.js"></script>
    <script src="../javascript/page_specific/mailbox.js"></script>
</body>
</html>