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
    <title>bsu : robots</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/bsu_general_style.css">
    <link rel="stylesheet" href="../css/theme.css">
    <link rel="icon" type="image/x-icon" href="../assets/svg/bsu_ai_icon.svg">
</head>
<body>
    <?php  Navigation::write_navigation("Robots Management"); ?>
    
    <div class="card">  
        <h2>Create New Robot</h2>
        <form id="createRobotForm">
            <div class="form-group">
                <label for="robotType">Robot Type</label>
                <select id="robotType" name="robotType" required>
                    <option value="jetank">Jetank</option>
                    <option value="dronebot">Dronebot</option>
                    <option value="carrier">Carrier</option>
                    <option value="jetracer">Jetracer</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="robotNamespace">Robot Namespace</label>
                <input type="text" id="robotNamespace" name="robotNamespace" placeholder="e.g., robot_zone1_001" required>
            </div>
            
            <div class="form-group checkbox-group">
                <input type="checkbox" id="robotStatus" name="robotStatus" checked>
                <label for="robotStatus">Active Status</label>
            </div>
            
            <button type="submit">Create Robot</button>
        </form>
    </div>
    
    <div class="card robot-list">
        <h2>Existing Robots</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Namespace</th>
                    <th>Creation date</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="robotTableBody">
                <!-- Loaded dynamically from API -->
            </tbody>
        </table>
    </div>

    <script src="../javascript/general_config.js"></script>
    <script src="../javascript/utils/themeToggle.js"></script>
    <script src="../javascript/utils/buildRobotCard.js"></script>
    <script src="../javascript/page_specific/robots.js"></script>
</body>
</html>