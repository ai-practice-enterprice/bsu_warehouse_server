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
    <title>bsu : zone occupancy</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/bsu_general_style.css">
    <link rel="stylesheet" href="../css/occupancy.css">
    <link rel="icon" type="image/x-icon" href="../assets/bsu_ai_icon.svg">
</head>
<body>
    <?php Navigation::write_navigation("Occupancy Management"); ?>
    
    <div class="card">
        <h2>Zone Availability</h2>
        <p>Click to enter an available zone or exit an occupied zone</p>

        <div class="form-group" style="flex: 1;">
            <label for="zoneType">Zone Type</label>
            <select id="zoneType" name="zoneType" required>
                <option value="DropZoneIn">Drop Zone (In)</option>
                <option value="DropZoneOut">Drop Zone (Out)</option>
                <option value="Storage">Storage Zone</option>
                <option value="ErrorZone">Error Zone</option>
                <option value="RobotStation">Robot Station</option>
            </select>
        </div>
        
        <div id="noZonesMessage" class="no-zones">
            <p>No zones available. Please create zones in the <a href="zones.html">Zone Management</a> page.</p>
        </div>
        
        <div id="zoneGrid" class="zone-grid">
            <!-- Will be populated with zone cards from API -->
        </div>
    </div>
    
    <script src="../javascript/general_config.js"></script>
    <script src="../javascript/utils/enterZone.js"></script>
    <script src="../javascript/utils/exitZone.js"></script>
    <script src="../javascript/utils/buildZoneCard.js"></script>
    <script src="../javascript/utils/buildSelectZoneType.js"></script>
    <script src="../javascript/page_specific/occupancy.js"></script>
</body>
</html>
