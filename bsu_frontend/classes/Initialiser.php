<?php
class Initialiser {
    private Controller $BSU_Controller; 

    function __construct()
    {
        define("ERRORLOG",LogHandler::$ERRORLOG); 

        // error handler =================================
        set_error_handler(function($errno, $errMsg, $errFile = "", $errLine = "", $errContext = ""){
        
            $error = "[ " . $errno . " ]: ";
            $error .= $errMsg;
            $error .= " in file " . $errFile;
            $error .= " on line " . $errLine ."\n";
            
            error_log($error, 3, ERRORLOG);
            exit();
        }, E_ALL);
        
        // exception handler =================================
        set_exception_handler(function($e){
            $handler = new LogHandler();
            $handler->writeErrorLog($e->getCode(), $e->getMessage(), $e->getFile(), $e->getLine());
            exit();
        });
        
        // class handler =================================
        // Load classes when used by the script
        // replaces the magic function "__autoload" for each class 
        // which means no implementation in the classes is required
        spl_autoload_register(function($className){

            $class = "./classes/".$className.".php";
            if(file_exists($class)){
                require_once($class);
                return true;
            }
             
        });

        $this->BSU_Controller = new Controller("bsu-db-server","webuser","PwdAIteamFrOnTenD2025","bsu_warehouse_db");
    }

    function startSession()
    {
        $result = session_start();
        
        if($result == false){
            require_once("./public/error.php");
            exit();
        }
    }
    
    function startChecks()
    {
        $this->BSU_Controller->checkConnection();

        $this->BSU_Controller->checkSession();

        if(!empty($_POST)){
            $this->BSU_Controller->checkPost();
            return;
        } 
        elseif(!empty($_GET)){
            $this->BSU_Controller->checkGet();
            return;
        }

        $this->BSU_Controller->defaultRedirection();

        return true;
    }
}
?>