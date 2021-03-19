<?php
  class patientAcc{
    private $fullName;
    private $NRIC;

    // constructor
    public function __construct($fullName, $NRIC) {
        $this->fullName= $fullName;
        $this->NRIC = $NRIC;
    }

    public function getfullName() {
        return $this->fullName;
    }

    public function getNRIC() {
      return $this->NRIC;
    }
   
}
?>