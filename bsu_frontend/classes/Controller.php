<?php
class Controller {
    private mysqli $DBC;
    private bool $loginStatus = false;

    function __construct($host,$userName,$pwd,$dbName)
    {
        $this->DBC = new mysqli($host,$userName,$pwd,$dbName);
    } ////////////////////////////////////////////////////////////////////////////////
    /*
    
    */
    function __destruct(){
        $this->DBC->close();
    } ////////////////////////////////////////////////////////////////////////////////
    /*
    
    */
    public function checkConnection(){
        if($this->DBC->connect_error){
            $handler = new LogHandler();
            $handler->writeWaringLog(1000,"Connection failed: ".$this->DBC->connect_error);
        }
    } ////////////////////////////////////////////////////////////////////////////////
    /*
          ______   ________   ______    ______   ______   ______   __    __ 
         /      \ /        | /      \  /      \ /      | /      \ /  \  /  |
        /$$$$$$  |$$$$$$$$/ /$$$$$$  |/$$$$$$  |$$$$$$/ /$$$$$$  |$$  \ $$ |
        $$ \__$$/ $$ |__    $$ \__$$/ $$ \__$$/   $$ |  $$ |  $$ |$$$  \$$ |
        $$      \ $$    |   $$      \ $$      \   $$ |  $$ |  $$ |$$$$  $$ |
         $$$$$$  |$$$$$/     $$$$$$  | $$$$$$  |  $$ |  $$ |  $$ |$$ $$ $$ |
        /  \__$$ |$$ |_____ /  \__$$ |/  \__$$ | _$$ |_ $$ \__$$ |$$ |$$$$ |
        $$    $$/ $$       |$$    $$/ $$    $$/ / $$   |$$    $$/ $$ | $$$ |
         $$$$$$/  $$$$$$$$/  $$$$$$/   $$$$$$/  $$$$$$/  $$$$$$/  $$/   $$/ 
    
    */
    public function checkSession(){
        if(isset($_SESSION["user_IP"]) && ($_SESSION["user_IP"] == $_SERVER["REMOTE_ADDR"]) && isset($_SESSION["user_ID"])){
            $this->loginStatus = true;
        } else {
            $_SESSION["user_IP"] = $_SERVER["REMOTE_ADDR"];
            $this->loginStatus = false;
        }

        return true;
    } ////////////////////////////////////////////////////////////////////////////////
    public function defaultRedirection(){
        // user fulfills all the checks of being a true user => logged in + admin  
        if($this->loginStatus == true && isset($_SESSION["isAdmin"]) && $_SESSION["isAdmin"]){
            $this->redirect("robots");
        } 
        // user fulfills all the checks of being a true user => logged in + NO admin 
        if($this->loginStatus == true && isset($_SESSION["isAdmin"]) && !$_SESSION["isAdmin"]) {
            $this->redirect("occupancy");
        }
        // in this last case i can not know what the user is so i have to send the user to the login page 
        // so that we can pick up his credentials again
        if($this->loginStatus == true && !isset($_SESSION["isAdmin"]) || $this->loginStatus == false) {
            $this->redirect("login");
        }

        return true;
    } ////////////////////////////////////////////////////////////////////////////////
    /*
         _______    ______    ______   ________ 
        /       \  /      \  /      \ /        |
        $$$$$$$  |/$$$$$$  |/$$$$$$  |$$$$$$$$/ 
        $$ |__$$ |$$ |  $$ |$$ \__$$/    $$ |   
        $$    $$/ $$ |  $$ |$$      \    $$ |   
        $$$$$$$/  $$ |  $$ | $$$$$$  |   $$ |   
        $$ |      $$ \__$$ |/  \__$$ |   $$ |   
        $$ |      $$    $$/ $$    $$/    $$ |   
        $$/        $$$$$$/   $$$$$$/     $$/    
    
    */
    public function checkPost(){
        if(isset($_POST["execute_request"])){
            switch ($_POST["execute_request"]) {
                case 'login':
                    $this->validateLogin();
                    break;
                case 'logout':
                    $this->validateLogout();
                    break;
                default:
                    break;
            }   
            return true;
        }
        return false;
    } ////////////////////////////////////////////////////////////////////////////////
    /*
          ______   ________  ________ 
         /      \ /        |/        |
        /$$$$$$  |$$$$$$$$/ $$$$$$$$/ 
        $$ | _$$/ $$ |__       $$ |   
        $$ |/    |$$    |      $$ |   
        $$ |$$$$ |$$$$$/       $$ |   
        $$ \__$$ |$$ |_____    $$ |   
        $$    $$/ $$       |   $$ |   
         $$$$$$/  $$$$$$$$/    $$/    
    */
    public function checkGet(){
        if(isset($_GET["navigate_to"])){
            $this->redirect($_GET["navigate_to"]);
            return true;
        }
        elseif (isset($_GET["logout"]) && $_GET["logout"]) {
            $this->validateLogout();
            return true;
        }
        return false;
    } ////////////////////////////////////////////////////////////////////////////////



    public function redirect($pageToRedirectTo){
        switch ($pageToRedirectTo) {
            case 'login':       
                require_once("./bsu/".$pageToRedirectTo.".php"); 
                break;
            case 'occupancy':   
                if($this->loginStatus == true){
                    require_once("./bsu/".$pageToRedirectTo.".php"); 
                } else {
                    require_once("./bsu/login.php"); 
                }
                break;
            case 'robots':      
            case 'packages':    
            case 'warehouse':   
            case 'zones':       
            case 'users':       
            case 'mailbox':       
                if($this->loginStatus == true){
                    require_once("./bsu/".$pageToRedirectTo.".php"); 
                } else {
                    require_once("./bsu/login.php"); 
                }
                break;
            case 'error':       
            case '404':         
                require_once("./public/".$pageToRedirectTo.".php"); break;
            default:
                require_once("../public/error.php");
                break;
        }
    } ////////////////////////////////////////////////////////////////////////////////
    public function JSONresponse($type,$messageCode = 0){
        $HTMLClass = $type."-message";
        $HTMLResponseData = null;
        $NewLocation = 0;
        if ($type == "warning") {
            switch ($messageCode) {
                case 100:
                    $HTMLResponseData = "Warning : Wrong login credentials : no user found";
                    break;
                case 101:
                    $HTMLResponseData = "Warning : Wrong login credentials : wrong password";
                    break;
                // add cases here...
                case 0:
                default:
                    $HTMLResponseData = "Warning : Message(0)!!";
                    break;
            }
        }
        elseif($type == "danger"){
            switch ($messageCode) {
                // add cases here...
                case 0:
                default:
                    $HTMLResponseData = "Danger : Message(0)";
                    break;
            }
        }
        elseif($type == "info"){
            switch ($messageCode) {
                // add cases here...
                case 0:
                default:
                    $HTMLResponseData = "Info : Message(0)";
                    break;
            }
        }
        elseif($type == "success"){
            switch ($messageCode) {
                case 100:
                    $HTMLResponseData = "Success : login complete";
                    $NewLocation = "robots";
                    break;
                case 101:
                    $HTMLResponseData = "Success : login complete";
                    $NewLocation = "occupancy";
                    break;
                // add cases here...
                case 0:
                default:
                    $HTMLResponseData = "Success : Message(0)";
                    break;
            }
        }
        else {
            return false;
        }

        $response = [
            "responseData" => $HTMLResponseData,
            "class" => $HTMLClass,
            "newlocation" => $NewLocation
        ];

        echo json_encode($response,JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_NUMERIC_CHECK);

        return true;
    } ////////////////////////////////////////////////////////////////////////////////
    public function validateLogout(){        
        $handler = new LogHandler();

        if(!session_unset()){
            return false;
        }

        if(!session_destroy()){
            return false;
        }

        if(isset($_SESSION["userName"])){
            $handler->writeLogOut($_SESSION["userName"]);
        }
        else {
            $handler->writeLogOut("unknown");
        }

        $this->loginStatus = false;
        $this->redirect("login");

        return true;
    } ////////////////////////////////////////////////////////////////////////////////
    public function validateLogin(){
        $queryValues = [];
        $formValues = $_POST["formClass"];

        foreach($_POST[$formValues] as $inputName => $inputValue ){
            $queryValues[$inputName] = htmlspecialchars($inputValue);
        }

        $queryConstructor = new QueryConstructor(
            "Users",
            [
                "select" => "*",
                "where"  => "Users.userName = ?" ,
            ],
            [
                $queryValues["userName"],
            ]
        );

        $resultQuery = $this->DBC->execute_query(
            $queryConstructor->select(),
            $queryConstructor->getQueryValues()
        );

        $fetchedRow = $resultQuery->fetch_assoc();

        if($resultQuery == false){
            $this->JSONresponse("warning");
            return false;
        } 
        
        if($resultQuery->num_rows == 0){
            $this->JSONresponse("warning",100);
            return false;
        } 

        if(!password_verify($queryValues["userPassword"],$fetchedRow["userPassword"])){
            $this->JSONresponse("warning",101);
            return false;
        }

        $_SESSION["user_ID"] = $fetchedRow["userID"];
        $_SESSION["userName"] = $fetchedRow["userName"];
        $this->loginStatus = true;

        $handler = new LogHandler();

        if($fetchedRow["adminPrivilege"] == true){
            $handler->writeLoginLog($fetchedRow["userName"]);
            $_SESSION["isAdmin"] = true;
            $this->JSONresponse("success",100);
        } else {
            $handler->writeLoginLog($fetchedRow["userName"]);
            $_SESSION["isAdmin"] = false;
            $this->JSONresponse("success",101);
        }

        return true;
    } ////////////////////////////////////////////////////////////////////////////////
}
?>