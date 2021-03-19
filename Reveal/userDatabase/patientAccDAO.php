<?php
class patientAccDAO {

    //check if patient is already registered with the clinic
    public function lookFor($Name) {
        $connMgr = new ConnectionManager();
        $conn = $connMgr->getConnection();

        $sql = "select Name from patientlogin where Name = :Name";
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':Name', $Name, PDO::PARAM_STR);

        $stmt->execute();
        $stmt->setFetchMode(PDO::FETCH_ASSOC);

		$user = false;
        if ($row = $stmt->fetch() ) {
            $user = true;
        }

        $stmt = null;
        $conn = null;
        
        return $user;
    }

    //retrieve fullName and NRIC to check at login
    public function loginCheck($Name) {
        $connMgr = new ConnectionManager();
        $conn = $connMgr->getConnection();

        $sql = "select NRIC from patientlogin where Name = :Name";
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':Name', $Name, PDO::PARAM_STR);

        $stmt->execute();
        $stmt->setFetchMode(PDO::FETCH_ASSOC);

		$ret = '';
        if ($row = $stmt->fetch() ) {
            $ret = $row['NRIC'];
        }

        $stmt = null;
        $conn = null;
        
        return $ret;
    }
    
}

?>
