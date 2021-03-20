<?php
    require_once('common.php');
    $Name = $_GET['Name'];
    $NRIC = $_GET['NRIC'];
    $patientAccDAO = new patientAccDAO;

    $result = $patientAccDAO->lookFor($Name);
    if($result){ //if username is in the database
        $NRIC_retrieved = $patientAccDAO->loginCheck($Name);
        
        if($NRIC != $NRIC_retrieved){
            echo 'false';
        } else{
            session_start();
            $_SESSION['Name']=$Name;
            $_SESSION['NRIC']=$NRIC;
            echo 'true';
        }
    } else{
        echo 'false';
    }
?>