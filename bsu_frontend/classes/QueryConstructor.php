<?php
/**
 * The query constructor handles and creates prepared MySQL queries
 * Such that only DML (data manipulation language) statments are allowed
 */
class QueryConstructor {
    private string $query = "";
    private string $queryTable = "";
    private array $queryValues = [];
    private array $queryClauses = [
        "select"        => "",
        "where"         => "" ,
        "order by"      => "",
        "inner join"    => [],
        "set"        => "",
    ];

    public function __construct(
        $queryTable = "",
        $queryClauses = [],
        $queryValues = []
    ){
        $this->queryClauses = $queryClauses;
        $this->queryTable = $queryTable;
        $counter = 0;
        foreach ($queryValues as $key => $value) {
            $this->queryValues[$counter] = $value;
            $counter++;
        }
    }

    public function setQueryTable(string $queryTable){
        $this->queryTable = $queryTable;
    }

    public function setQueryValues(array $queryValues){
        $this->queryValues = array();
        $counter = 0;
        foreach ($queryValues as $key => $value) {
            $this->queryValues[$counter] = $value;
            $counter++;
        }
    }

    public function getValue(string $value){
        if(isset($this->queryValues[$value])){
            return $this->queryValues[$value];
        }
        return false;
    }

    public function setQueryClauses(array $queryClauses){
        $this->queryClauses = $queryClauses;
    }

    public function getQueryTable(){
        return $this->queryTable;
    }

    public function getQueryValues(){
        return $this->queryValues;
    }

    public function getQueryClauses(){
        return $this->queryClauses;
    }

    public function update(){
        $this->query = "UPDATE ".$this->queryTable;

        if(isset($this->queryClauses["set"]) && !empty($this->queryClauses["set"])){
            $this->query .= " SET ".$this->queryClauses["set"];
        } else {
            return false;
        }

        if(isset($this->queryClauses["where"]) && !empty($this->queryClauses["where"])){
            $this->query .= " WHERE ".$this->queryClauses["where"];
        } else {
            return false;
        }
        return $this->query;
    }
    
    public function select(){
        $this->query = "";
        if(isset($this->queryClauses["select"]) && !empty($this->queryClauses["select"])){
            $this->query .= "SELECT ".$this->queryClauses["select"]." FROM ".$this->queryTable;
        } else {
            return false;
        }

        if(isset($this->queryClauses["inner join"]) && !empty($this->queryClauses["inner join"])){
            foreach ($this->queryClauses["inner join"] as $remoteTable => $table) {
                $this->query .= " INNER JOIN ".$remoteTable." ON $table[0] = $table[1]";
            }
        }
        
        if(isset($this->queryClauses["where"]) && !empty($this->queryClauses["where"])){
            $this->query .= " WHERE ".$this->queryClauses["where"];
        }
        
        if(isset($this->queryClauses["order by"]) && !empty($this->queryClauses["order by"])){
            $this->query .= " ORDER BY ".$this->queryClauses["order by"];
        }

        return $this->query;
    }
    
    public function delete(){
        $this->query = "";
        $this->query .= "DELETE FROM ".$this->queryTable;
        if(isset($this->queryClauses["where"]) && !empty($this->queryClauses["where"])){
            $this->query .= " WHERE ".$this->queryClauses["where"];
        } else {
            return false;
        }
        return $this->query;
    }
    
    public function insert($columns,$valuesPlaceholders){
        $this->query = "";
        $this->query .= "INSERT INTO ".$this->queryTable."(".$columns.")";
        $this->query .= " VALUES (".$valuesPlaceholders.")";
        return $this->query;
    }

}

?>