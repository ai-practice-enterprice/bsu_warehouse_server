CREATE DATABASE IF NOT EXISTS bsu_warehouse_db;

CREATE USER "aiUser"@"bsu-api-server" IDENTIFIED BY "pwdAIteamDB";
CREATE USER "webuser"@"%" IDENTIFIED BY "PwdAIteamFrOnTenD2025";

GRANT SELECT, INSERT, UPDATE ON bsu_warehouse_db.* TO "aiUser"@"bsu-api-server";
GRANT SELECT ON bsu_warehouse_db.* TO "webuser"@"%";



