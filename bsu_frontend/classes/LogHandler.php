<?php
class LogHandler extends Exception {

    public static $LOGINLOG = "./private/login/login.log";
    public static $LOGOUTLOG = "./private/logout/logout.log";
    public static $WARNINGLOG = "./private/warning/warning.log";
    public static $ERRORLOG = "./private/error/error.log";
    public static $HISTORYLOG = "./private/history/history.log";


    function __construct()
    {
        
    } 

    private function resolveLogPath($logFileName) {
        $paths = [
            "{$logFileName}",
            ".{$logFileName}"
        ];

        foreach ($paths as $path) {
            if (is_writable($path)) {
                return $path;
            }
        }

        return null;
    }

    public function writeLoginLog($userName) {
        $login = "{$userName} logged in at :\t " . date("Y-m-d H:i:s - ") . "\n";

        $path = $this->resolveLogPath(self::$LOGINLOG);

        if (!file_exists($path)) {
            $loginFile = fopen($path, "w");
        }
        else {
            $loginFile = fopen($path, "a");
        }

        fwrite($loginFile, $login);
        fclose($loginFile);
    }

    public function writeLogOut($userName) {
        $logout = "{$userName} logged out at :\t " . date("Y-m-d H:i:s - ") . "\n";
        $path = $this->resolveLogPath(self::$LOGOUTLOG);
        if (!file_exists($path)) {
            $logoutFile = fopen($path, "w");
        }
        else {
            $logoutFile = fopen($path, "a");
        }

        fwrite($logoutFile, $logout);
        fclose($logoutFile);
    }

    public function writeWaringLog($warnNo,$warnMsg){
        $warning = "[ " . $warnNo . " ]: ";
        $warning .= $warnMsg;
        $warning .= " at time : " . date("Y-m-d H:i:s - ") . "\n";
        $path = $this->resolveLogPath(self::$WARNINGLOG);
        if (!file_exists($path)) {
            $warningFile = fopen($path, "w");
        }
        else {
            $warningFile = fopen($path, "a");
        }

        fwrite($warningFile, $warning);
        fclose($warningFile);
    }

    public function writeErrorLog($errno, $errMsg, $errFile = "", $errLine = "") {
        $error = "[ " . $errno . " ]: ";
        $error .= $errMsg;
        $error .= " in file : " . $errFile . "\t";
        $error .= " on line : " . $errLine . "\t";
        $error .= " at time : " . date("Y-m-d H:i:s - ") . "\n";
        $path = $this->resolveLogPath(self::$ERRORLOG);
        error_log($error, 3, $path);
    }

    public function writeHistoryLog($hisMsg,$hisAction) {
        $history = " at time : " . date("Y-m-d H:i:s - ") . "\t";
        $history .= " User : "; 
        if(isset($_SESSION["userName"])){ 
            $history .= $_SESSION['userName'] . "\t";
        } 
        else { 
            $history .= "Unknown" . "\t" ;
        }
        if(!empty($hisMsg)){
            $history .= " Message : " . $hisMsg . "\t";
        }
        $history .= " Action : " . $hisAction . "\n";

        $path = $this->resolveLogPath(self::$HISTORYLOG);
        if(!file_exists($path)){
            $historyFile = fopen($path, "w");
        }
        else {
            $historyFile = fopen($path, "a");
        }

        fwrite($historyFile, $history);
        fclose($historyFile);
    }
}
?>