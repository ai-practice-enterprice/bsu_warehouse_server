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
    <title>bsu : Users</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/bsu_general_style.css">
    <link rel="icon" type="image/x-icon" href="../assets/svg/bsu_ai_icon.svg">
</head>
<body>
    <?php  Navigation::write_navigation("User Management"); ?>

    <div class="card">  
        <h2>Add User</h2>
        <form id="createUserForm">
            <div class="form-group">
                <label for="adminPrivilege">User Type</label>
                <select id="adminPrivilege" name="adminPrivilege" required>
                    <option value="true">Admin</option>
                    <option value="false">Worker</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="userName">Username</label>
                <input type="email" id="userName" name="userName" placeholder="e.g., john.doe@blueskyunlimited" required>
            </div>

            <div class="form-group">
                <label for="userPassword">User password</label>
                <input type="password" id="userPassword" name="userPassword" required>
            </div>
            
            <div class="form-group checkbox-group">
                <input type="checkbox" id="userStatus" name="userStatus" checked>
                <label for="userStatus">Active Status</label>
            </div>
            
            <button type="submit">Create User</button>
        </form>
    </div>

    <div class="card" id="user-container">
        <table id="userTable">
            <tr>
                <th>UserID</th>
                <th>Email address</th>
                <th>Registration date</th>
                <th>privilege</th>
                <th>Status</th>
                <th></th>
            </tr>
            <!-- Will be populated with API -->
        </table>
    </div>

    <script>
        var current_user_id = <?php echo $_SESSION["user_ID"] ?>;
    </script>
    <script src="../javascript/general_config.js"></script>
    <script src="../javascript/libraries/d3.js"></script>
    <script src="../javascript/libraries/plot.js"></script>
    <script src="../javascript/utils/buildUserCard.js"></script>
    <script src="../javascript/page_specific/users.js"></script>
</body>
</html>