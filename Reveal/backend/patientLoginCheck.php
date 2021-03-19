<?php
    require_once('common.php');
    $fullName = $_GET['fullName'];
    $NRIC = $_GET['NRIC'];
    $patientAccDAO = new patientAccDAO;

    $result = $patientAccDAO->lookFor($fullName);
    if($result){ //if username is in the database
        $NRIC_retrieved = $patientAccDAO->loginCheck($fullName);
        
        if($NRIC != $NRIC_retrieved){
            echo 'false';
        } else{
            session_start();
            $_SESSION['fullName']=$fullName;
            $_SESSION['NRIC']=$NRIC;
            echo 'true';
        }
    } else{
        echo 'false';
    }
?>