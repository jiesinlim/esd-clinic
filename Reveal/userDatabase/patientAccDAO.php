<?php
class patientAccDAO {

    //check if patient is already registered with the clinic
    public function lookFor($fullName) {
        $connMgr = new ConnectionManager();
        $conn = $connMgr->getConnection();

        $sql = "select fullName from patientlogin where fullName = :fullName";
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':fullName', $fullName, PDO::PARAM_STR);

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
    public function loginCheck($fullName) {
        $connMgr = new ConnectionManager();
        $conn = $connMgr->getConnection();

        $sql = "select NRIC from patientlogin where fullName = :fullName";
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':fullName', $fullName, PDO::PARAM_STR);

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
