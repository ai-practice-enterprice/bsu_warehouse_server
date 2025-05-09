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
    <title>bsu : login</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/bsu_general_style.css">
    <link rel="stylesheet" href="../css/login.css">
    <link rel="icon" type="image/x-icon" href="../assets/svg/bsu_ai_icon.svg">
</head>
<body>
    <div class="card card-group">
        <div class="card icon-container">
            <img src="../assets/svg/bsu_ai_dep.svg" alt="icon AI dept">
        </div>
        <div class="card">
            <h1 id="main-title">Blue Sky Unlimited :<br> AI departement</h1>
        </div>
    </div>
    <div class="card">
        <form class="loginForm">
            <label for="input-username">Username</label>
            <input type="text" id="input-username" name="loginForm[userName]">
            <label for="input-userpassword">Password</label>
            <input type="text" id="input-userpassword" name="loginForm[userPassword]">
            <input type="submit" value="Login" name="form" data-inputID="login" class="primary-btn">
        </form>
    </div>
    <div class="card" id="responseCard"></div>

    <script src="../javascript/page_specific/login.js"></script>
</body>
</html>