<?php
class Navigation {

    private $m_title; 

    function __construct($title)
    {
        $this->m_title = $title;
    }

    static function write_navigation($title)
    {
        if(isset($_SESSION["isAdmin"]) && $_SESSION["isAdmin"]){
        ?>
        <div class="header" id="navigation-menu">
            <h1><?php echo $title; ?></h1>
            <div class="nav-links">
                <a href="./bsu.php?navigate_to=robots">&Ropf; Robots</a>
                <a href="./bsu.php?navigate_to=zones">&Zopf; Zones</a>
                <a href="./bsu.php?navigate_to=occupancy">&Oopf; Occupancy</a>
                <a href="./bsu.php?navigate_to=packages">&Popf; Packages</a>
                <a href="./bsu.php?navigate_to=warehouse">&Wopf; Warehouse</a>
                <a href="./bsu.php?navigate_to=users">&Uopf; Users</a>
                <a href="./bsu.php?navigate_to=mailbox">&Mopf; Mailbox</a>
                <a href="./bsu.php?logout=true">&rarrhk; Logout</a>
            </div>
        </div>
        <?php
        } else {
            ?>
            <div class="header" id="navigation-menu">
                <h1><?php echo $title; ?></h1>
                <a href="./bsu.php?logout=true">&rarrhk; Logout</a>
            </div>
            <?php
        }
    }
}

?>