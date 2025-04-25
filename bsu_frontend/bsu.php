<?php
    define("APP_STARTED",true);
    // in order for the Initialiser to be loaded i still need to do it statically
    // but all the other classes are loaded dynamically after because of the 
    require_once("./classes/LogHandler.php");
    require_once("./classes/Initialiser.php");

    $init = new Initialiser();
    $init->startSession();
    $init->startChecks();
?>
