<?php
require_once("./classes/QueryConstructor.php");
$DBC = new mysqli("bsu-db-server","webuser","PwdAIteamFrOnTenD2025","bsu_warehouse_db");

$queryConstructor = new QueryConstructor(
    "Users",
    [
        "select" => "*",
    ]
);

$resultQuery = $DBC->execute_query(
    $queryConstructor->select(),
    $queryConstructor->getQueryValues()
);


for($i = 0;$i < $resultQuery->num_rows;$i++){
    $fetchedRow = $resultQuery->fetch_assoc();
    var_dump($fetchedRow);
}
