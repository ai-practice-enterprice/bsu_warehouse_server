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
    <title>BSU : Warehouse</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="./css/bsu_general_style.css">
    <link rel="stylesheet" href="./css/warehouse.css">
    <link rel="stylesheet" href="css/occupancy.css">
    <link rel="icon" type="image/x-icon" href="./assets/svg/bsu_ai_icon.svg">
</head>
<body>
    <?php  Navigation::write_navigation("Warehouse Management"); ?>

    <div class="form-group" style="flex: 1;">
        <div class="flex-group">
            <div class="card" id="warehouse_map">  
                <!-- Will be populated with API -->
            </div>
            <div class="card" id="data-holder">
                <!-- Will be populated with API -->
            </div>
        </div>
        <div class="card zonedata">
            <!-- Will be populated with API -->
        </div>
    </div>

    <script src="../javascript/general_config.js"></script>
    <script src="../javascript/libraries/d3.js"></script>
    <script src="../javascript/libraries/plot.js"></script>
    <script src="../javascript/utils/buildSelectZoneType.js"></script>
    <script src="../javascript/utils/buildZoneCard.js"></script>
    <script src="../javascript/page_specific/warehouse.js"></script>
</body>
</html>